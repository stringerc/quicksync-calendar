# Contributing to Django OAuth Hub

We love your input! We want to make contributing to Django OAuth Hub as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

## Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

## Setting Up Development Environment

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/django_oauth_hub.git
   cd django_oauth_hub
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If exists
   ```

4. **Set up environment**
   ```bash
   cp .env.example .env
   # Edit .env with your test credentials
   ```

5. **Run migrations**
   ```bash
   python manage.py migrate
   ```

6. **Run tests**
   ```bash
   python manage.py test
   ```

## Coding Standards

- Follow PEP 8 style guide for Python code
- Use meaningful variable and function names
- Add docstrings to all functions and classes
- Comment complex logic
- Keep functions small and focused
- Use type hints where appropriate

## Testing

- Write tests for new functionality
- Ensure existing tests pass
- Maintain good test coverage
- Test both success and error cases
- Include integration tests for OAuth flows

## Adding New OAuth Platforms

To add support for a new OAuth platform:

1. **Update Platform Choices**
   - Add platform to `PLATFORM_CHOICES` in `models.py`
   - Add configuration to `OAUTH_PLATFORMS` in `settings.py`

2. **Update Templates**
   - Add platform icon and styling
   - Update dashboard template

3. **Platform-Specific Logic**
   - Add any platform-specific token exchange logic
   - Handle platform-specific user info format
   - Add platform-specific error handling

4. **Documentation**
   - Update README.md with setup instructions
   - Add platform to supported platforms list
   - Update deployment guide

5. **Tests**
   - Add platform-specific tests
   - Test OAuth flow integration
   - Test error handling

## Security Considerations

When contributing, please consider:

- Never commit secrets or API keys
- Use environment variables for configuration
- Validate all user inputs
- Follow OAuth 2.0 security best practices
- Implement proper error handling without information leakage
- Use HTTPS for all OAuth redirects
- Implement CSRF protection

## Documentation

- Update README.md for new features
- Update DEPLOYMENT.md for deployment changes
- Add inline code comments for complex logic
- Update docstrings for API changes

## Reporting Bugs

We use GitHub issues to track public bugs. Report a bug by opening a new issue.

**Great Bug Reports** tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

## Feature Requests

We welcome feature requests! Please:

1. Check if the feature already exists or is planned
2. Open a GitHub issue describing the feature
3. Explain the use case and why it would be valuable
4. Be willing to contribute to the implementation

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Code of Conduct

This project and everyone participating in it is governed by a Code of Conduct. By participating, you are expected to uphold this code.

### Our Pledge

We pledge to make participation in our project a harassment-free experience for everyone, regardless of age, body size, disability, ethnicity, gender identity and expression, level of experience, nationality, personal appearance, race, religion, or sexual identity and orientation.

### Our Standards

**Positive behavior includes:**
- Using welcoming and inclusive language
- Being respectful of differing viewpoints and experiences
- Gracefully accepting constructive criticism
- Focusing on what is best for the community
- Showing empathy towards other community members

**Unacceptable behavior includes:**
- The use of sexualized language or imagery and unwelcome sexual attention or advances
- Trolling, insulting/derogatory comments, and personal or political attacks
- Public or private harassment
- Publishing others' private information without explicit permission
- Other conduct which could reasonably be considered inappropriate in a professional setting

## Questions?

Feel free to reach out if you have any questions about contributing!
