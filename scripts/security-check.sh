#!/bin/bash

# Security Check Script for AITutor
echo "🔒 Running security audit..."

# Check for exposed API keys
echo "🔍 Checking for exposed API keys..."
if grep -r "sk-or-v1-" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=venv --exclude="*.md" --exclude="*.sh"; then
    echo "❌ EXPOSED API KEY FOUND!"
    exit 1
else
    echo "✅ No exposed API keys found"
fi

# Check for .env files in git
echo "🔍 Checking for .env files in git..."
if git ls-files | grep -E "\.env[^.]"; then
    echo "❌ .ENV FILES COMMITTED TO GIT!"
    exit 1
else
    echo "✅ No .env files in git"
fi

# Check for hardcoded secrets
echo "🔍 Checking for hardcoded secrets..."
if grep -r -i "password\|secret\|token.*=" . --exclude-dir=node_modules --exclude-dir=.git --exclude-dir=venv --exclude="*.md" --exclude="*.sh"; then
    echo "❌ POTENTIAL SECRETS FOUND!"
    exit 1
else
    echo "✅ No hardcoded secrets found"
fi

# Check file permissions
echo "🔍 Checking file permissions..."
if find . -type f -name "*.sh" -not -perm -u+x; then
    echo "⚠️  Some shell files are not executable"
fi

# Check for sensitive file extensions
echo "🔍 Checking for sensitive files..."
if find . -name "*.key" -o -name "*.pem" -o -name "*.p12" | grep -v node_modules; then
    echo "❌ SENSITIVE FILES FOUND!"
    exit 1
else
    echo "✅ No sensitive files found"
fi

echo "✅ Security audit complete!"
echo "📋 Security checklist:"
echo "  ✅ No exposed API keys"
echo "  ✅ No .env files in git"
echo "  ✅ No hardcoded secrets"
echo "  ✅ No sensitive files"
echo ""
echo "🚀 Application is secure for deployment!"
