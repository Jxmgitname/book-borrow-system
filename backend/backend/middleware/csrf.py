class DisableCSRFForAPIMiddleware:
    """JWT 接口走 Authorization 头，对 /api/ 路径关闭 CSRF 校验。"""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.path.startswith('/api/'):
            setattr(request, '_dont_enforce_csrf_checks', True)
        return self.get_response(request)
