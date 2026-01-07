# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Security Best Practices

### Before Deployment

1. **Change Secret Key**
   - Never use the default secret key in production
   - Generate a strong random key: `python -c "import secrets; print(secrets.token_hex(32))"`
   - Set as environment variable: `SECRET_KEY`

2. **Environment Variables**
   - Never commit `.env` files
   - Use environment variables for all sensitive data
   - API keys should be in environment variables only

3. **Database Security**
   - Use PostgreSQL in production (not SQLite)
   - Use strong database passwords
   - Enable database encryption
   - Regular backups

4. **API Keys**
   - Never hardcode API keys
   - Use environment variables
   - Rotate keys regularly
   - Use different keys for dev/prod

5. **HTTPS**
   - Always use HTTPS in production
   - Never send sensitive data over HTTP
   - Use proper SSL certificates

### Data Protection

- **User Data**: Isolated by user_id
- **Passwords**: Hashed using Werkzeug (never stored plain text)
- **Sessions**: Secure session management
- **Input Validation**: All user inputs validated
- **SQL Injection**: Prevented with parameterized queries

### Reporting a Vulnerability

If you discover a security vulnerability, please:
1. **Do NOT** open a public issue
2. Email security details to: [your-email]
3. Include:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

We will respond within 48 hours.

## Security Checklist

- [ ] Secret key changed from default
- [ ] Environment variables configured
- [ ] No API keys in code
- [ ] Database properly secured
- [ ] HTTPS enabled
- [ ] Input validation in place
- [ ] Error messages don't expose internals
- [ ] Regular security updates
- [ ] Dependencies up to date

