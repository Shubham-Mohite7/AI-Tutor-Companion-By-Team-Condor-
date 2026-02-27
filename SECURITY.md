# Security Policy

## 🔐 Security Overview

This document outlines security measures and vulnerabilities for the AITutor application.

## 🚨 Critical Security Issues Fixed

### 1. **Exposed API Key** - FIXED ✅
- **Issue**: Real OpenRouter API key was exposed in `.env.save` file
- **Fix**: Removed the file and updated documentation
- **Impact**: Prevents unauthorized API usage

### 2. **Repository Information Leakage** - FIXED ✅
- **Issue**: GitHub repository URL exposed in API headers
- **Fix**: Changed to generic domain `https://aitutor.app`
- **Impact**: Prevents repository discovery

## 🛡️ Security Measures Implemented

### Environment Variables
- ✅ All `.env` files properly ignored in `.gitignore`
- ✅ API keys never committed to repository
- ✅ Environment-specific configurations

### CORS Configuration
- ✅ Restricted to specific origins in production
- ✅ Proper preflight request handling
- ✅ Development vs production separation

### API Security
- ✅ No sensitive data in client-side code
- ✅ API keys stored server-side only
- ✅ Proper error handling without information leakage

### Input Validation
- ✅ Sanitized user inputs
- ✅ Type checking with Pydantic models
- ✅ SQL injection prevention (no database used)

## 🔍 Security Checklist

### ✅ Completed
- [x] Remove exposed API keys
- [x] Secure environment variable handling
- [x] CORS configuration
- [x] Input validation
- [x] Error message sanitization
- [x] Git ignore security files
- [x] Remove repository URLs from headers

### 🔄 Recommended for Production
- [ ] Rate limiting on API endpoints
- [ ] Request size limits
- [ ] HTTPS enforcement
- [ ] Content Security Policy (CSP)
- [ ] API authentication (if needed)
- [ ] Logging and monitoring
- [ ] Regular security audits

## 🚀 Production Security Recommendations

### 1. Environment Variables
```bash
# Use environment-specific files
cp .env.example .env.production
# Add your actual API keys to .env.production only
```

### 2. Docker Security
```yaml
# Use non-root user
USER appuser
# Read-only filesystem where possible
READ_ONLY: true
```

### 3. Network Security
- Use VPN or private networks
- Implement firewall rules
- Regular security updates

### 4. Monitoring
- Set up error tracking
- Monitor API usage
- Alert on suspicious activity

## 🔐 API Key Management

### OpenRouter API Key
- **Location**: Server-side environment variable only
- **Access**: Backend service only
- **Rotation**: Recommended every 90 days
- **Storage**: Never in code or version control

### Environment Setup
```bash
# Development
export OPENROUTER_API_KEY="your_dev_key"

# Production
export OPENROUTER_API_KEY="your_prod_key"
```

## 🚨 Reporting Security Issues

If you discover a security vulnerability:

1. **Do NOT** open a public issue
2. Email: security@aitutor.app
3. Include detailed description and reproduction steps
4. We'll respond within 48 hours

## 📋 Security Best Practices

### Development
- Never commit API keys
- Use environment variables
- Regular dependency updates
- Code reviews for security

### Deployment
- HTTPS only
- Environment separation
- Regular backups
- Security monitoring

### Operations
- Principle of least privilege
- Regular security audits
- Incident response plan
- User access controls

---

**Last Updated**: 2026-02-27
**Next Review**: 2026-03-27
