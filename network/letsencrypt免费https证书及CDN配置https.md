使用场景:

- 通过letsencrypt获取免费https证书
- 使用阿里云的CDN，支持https协议
- 证书3个月有效期，每3个月要重新获取证书，并更新到CDN配置

# 通过letsencrypt获取免费https证书

# 阿里云CDN配置https协议

# 每3个月更新证书

配置CDN时把域名配置为CNAME方式，指向了阿里云地址，分为4步走

- 更新证书前，需要临时把域名改为A方式(临时取消CDN缓存,但服务能正常访问)
- 更新https证书，验证ok（此时CDN还没有生效）
- 更新阿里云CDN的https配置(此时CDN还没有生效)
- 再把域名改为CNAME方式，指向阿里云的CDN服务器(CDN缓存重新生效)


