// URL bases
export const UrlBase        = "http://localhost:3000/api"
export const AuthUrlBase    = UrlBase.concat("/auth")
export const RouteUrlBase    = UrlBase.concat("/route")
export const VideoUrlBase   = UrlBase.concat("/video")
export const RequestUrlBase = UrlBase.concat("/request")
export const LocationUrlBase = UrlBase.concat("/location")
export const CustomerUrlBase = UrlBase.concat("/customer")

// Customer Auth Urls
export const CustomerLoginUrl    = AuthUrlBase.concat("/login")
export const CustomerRegisterUrl = AuthUrlBase.concat("/register")

// Customer Video Urls
export const VideoPostUrl    = VideoUrlBase.concat("/upload")
export const VideoDisplayUrl = VideoUrlBase.concat("/display/")
export const VideoDeleteUrl = VideoUrlBase.concat("/delete/")

// Customer Request Urls
export const RequestSendUrl = RequestUrlBase.concat("/send")
export const RequestEditUrl = RequestUrlBase.concat("/edit/")

// Admin Auth Urls
export const AdminLoginUrl    = AuthUrlBase.concat("/admin_login")

// Location Urls
export const LocationSendUrl = LocationUrlBase.concat("/send")

// customer Urls
export const CustomerMetricsUrl = CustomerUrlBase.concat("/metrics")
