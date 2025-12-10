#!/bin/sh
set -e

# 환경 변수 확인
if [ -n "$CADDY_DOMAIN" ]; then
    echo "=========================================="
    echo "Production mode: Domain is set to $CADDY_DOMAIN"
    echo "Auto HTTPS will be enabled"
    echo "=========================================="
    
    # 프로덕션 모드 Caddyfile 생성
    # HTTP-01 챌린지 사용 (포트 80이 외부에서 접근 가능해야 함)
    cat > /etc/caddy/Caddyfile << EOF
{
	auto_https on
}

# HTTP to HTTPS 리다이렉트
$CADDY_DOMAIN {
	redir https://{host}{uri} permanent
}

# HTTPS 서버 (Let's Encrypt 자동 인증서 발급)
# HTTP-01 챌린지 사용 (기본값, 포트 80 접근 필요)
https://$CADDY_DOMAIN {
	root * /usr/share/caddy

	handle /api/* {
		reverse_proxy backend:8000 {
			header_up Host {host}
			header_up X-Real-IP {remote}
			header_up X-Forwarded-For {remote}
			header_up X-Forwarded-Proto {scheme}
		}
	}

	# /translation_demo_web 경로 처리 (이전 빌드 호환성)
	handle /translation_demo_web/* {
		uri strip_prefix /translation_demo_web
		try_files {path} /index.html
		file_server
	}

	@static {
		path *.js *.css *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2 *.ttf *.eot *.webp *.avif
	}
	handle @static {
		header Cache-Control "public, max-age=31536000, immutable"
		file_server
	}

	try_files {path} /index.html
	file_server

	encode gzip
}
EOF
else
    echo "=========================================="
    echo "Development mode: No domain set"
    echo "Using HTTP only on port 80"
    echo "=========================================="
    
    # 개발 모드용 Caddyfile 생성
    cat > /etc/caddy/Caddyfile << 'EOF'
{
	auto_https off
}

:80 {
	root * /usr/share/caddy

	handle /api/* {
		reverse_proxy backend:8000 {
			header_up Host {host}
			header_up X-Real-IP {remote}
			header_up X-Forwarded-For {remote}
			header_up X-Forwarded-Proto {scheme}
		}
	}

	# /translation_demo_web 경로 처리 (이전 빌드 호환성)
	handle /translation_demo_web/* {
		uri strip_prefix /translation_demo_web
		try_files {path} /index.html
		file_server
	}

	@static {
		path *.js *.css *.png *.jpg *.jpeg *.gif *.ico *.svg *.woff *.woff2 *.ttf *.eot *.webp *.avif
	}
	handle @static {
		header Cache-Control "public, max-age=31536000, immutable"
		file_server
	}

	try_files {path} /index.html
	file_server

	encode gzip
}
EOF
fi

echo ""
echo "Generated Caddyfile:"
echo "=========================================="
cat /etc/caddy/Caddyfile
echo "=========================================="
echo ""

# Caddy 실행
exec caddy run --config /etc/caddy/Caddyfile
