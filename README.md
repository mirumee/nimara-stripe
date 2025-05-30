# Nimara Stripe

Integration between Stripe and Saleor for payment processing and tax calculations.

## Features

- **Payment Processing**: Seamless integration with Stripe Payment Intents
- **Multi-channel Support**: Configure different Stripe accounts for each Saleor channel
- **Tax Calculation**: Automated tax calculations using Stripe Tax
- **Webhook Support**: Full support for Stripe webhooks to handle payment status updates
- **Fully Typed**: Complete type checking with MyPy for better code reliability

## Requirements

### Development
- Python 3.12+
- [UV](https://docs.astral.sh/uv/getting-started/installation/) package manager
- [Docker](https://www.docker.com/) and Docker Compose
- [Localstack](https://docs.localstack.cloud/overview/) (for local AWS services)
- [Stripe account](https://dashboard.stripe.com/)

### Production
- [AWS Account](https://aws.amazon.com/) with appropriate IAM permissions
- [OpenTofu](https://opentofu.org/docs/intro/install/) (or Terraform) for infrastructure management
- [Stripe account](https://dashboard.stripe.com/) with API keys configured

## Local Development

### 1. Clone the repository

```bash
git clone https://github.com/mirumee/nimara-stripe.git
cd nimara-stripe
```

### 2. Set up environment

Copy the example environment file and update it with your specific values:

```bash
cp .env.example .env
```

### 3. Start the application

Using Docker Compose:

```bash
docker compose run --rm -P app
```

The application will be exposed on port 8080 by default.

## Configuration

### App installation

1. Deploy the app to your environment
2. Install the app in your Saleor instance
3. Set up a webhook in Stripe:
   - URL: `https://<YOUR_DOMAIN>/payment/webhook`
   - Listen for payment_intent.* events

### Saleor Configuration

Open the app dashboard in Saleor and configure:
- Stripe public key
- Stripe secret key
- Stripe webhook secret key

Configure these settings for each channel you want to use with Stripe.

## Development

### Running tests

```bash
make test
```

### Code quality checks

```bash
make check
```

### Building Lambda packages

```bash
make all
```

## Deployment

Please check out our [Deployment Guide](docs/DEPLOYMENT.md) for more details.

## Contributing

Contributions are welcome! Please check out our [Contributing Guide](CONTRIBUTING.md) for more details.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Run `make check` to ensure all tests and linting pass
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## License

This project is licensed under the BSD 3-Clause License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Saleor](https://saleor.io/) - The e-commerce platform
- [Stripe](https://stripe.com/) - Online payment processing for internet businesses

---

## ❤️ Community & Contribution

Join Nimara community on [GitHub Discussions](https://github.com/mirumee/nimara-stripe/discussions) and [Discord server](https://discord.gg/w4V3PZxGDj). You can ask questions, report bugs, participate in discussions, share ideas or make feature requests.

You can also contribute to Nimara in various ways:

- Report [issues](https://github.com/mirumee/nimara-stripe/issues/new?assignees=srinivaspendem%2Cpushya22&labels=%F0%9F%90%9Bbug&projects=&template=--bug-report.yaml&title=%5Bbug%5D%3A+) and suggest [new features](https://github.com/mirumee/nimara-stripe/issues/new?assignees=srinivaspendem%2Cpushya22&labels=%E2%9C%A8feature&projects=&template=--feature-request.yaml&title=%5Bfeature%5D%3A+).
- Review [documentation](https://nimara-docs.vercel.app/) and submit [pull requests](https://github.com/mirumee/nimara-stripe/pulls)—whether it's fixing typos or adding new features.
- Share your experiences or projects related to Nimara with the broader community through talks or blog posts.
- Support [popular feature requests](https://github.com/mirumee/nimara-stripe/issues?q=sort%3Aupdated-desc+is%3Aissue+is%3Aopen) by upvoting them.

<div align="center"> <strong>Crafted with ❤️ by Mirumee Software</strong>

[hello@mirumee.com](mailto:hello@mirumee.com)

</div>
