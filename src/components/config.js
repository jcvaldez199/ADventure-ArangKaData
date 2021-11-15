// URL bases
export const UrlBase        = "http://localhost:3000/api"
export const AuthUrlBase    = UrlBase.concat("/auth")
export const RouteUrlBase    = UrlBase.concat("/route")
export const VideoUrlBase   = UrlBase.concat("/video")
export const RequestUrlBase = UrlBase.concat("/request")

// Customer Auth Urls
export const CustomerLoginUrl    = AuthUrlBase.concat("/login")
export const CustomerRegisterUrl = AuthUrlBase.concat("/register")

// Customer Video Urls
export const VideoPostUrl    = VideoUrlBase.concat("/upload")
export const VideoDisplayUrl = VideoUrlBase.concat("/display/")

// Customer Request Urls
export const RequestSendUrl = RequestUrlBase.concat("/send")
export const RequestEditUrl = RequestUrlBase.concat("/edit/")

// Admin Auth Urls
export const AdminLoginUrl    = AuthUrlBase.concat("/admin_login")
