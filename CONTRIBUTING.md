# Contributing to nimara-stripe

Thank you for considering contributing to nimara-stripe!

We welcome all contributions, whether they be code, documentation, bug reports, or any other help you can provide.

## Getting Started

1. **Fork the Repository**:

   - Click the "Fork" button at the top of this repository and clone your fork locally:

     ```bash
     git clone https://github.com/mirumee/nimara-stripe.git
     ```

   - Navigate to your local repository:

     ```bash
     cd nimara-stripe
     ```

2. **Set Upstream**:

   - Add the original repository as a remote to keep your fork in sync:

     ```bash
     git remote add upstream https://github.com/mirumee/nimara-stripe.git
     git fetch upstream
     ```

3. **Create a Branch**:

   - Always create a new branch for your work:

     ```bash
     git checkout -b feature/your-feature-name
     ```

## Making Changes

1. **Code Standards**:

   - Ensure your code adheres to the project's coding standards.
   - Run formatting and linting before committing:

     ```bash
     make format
     make lint
     ```

   - Write clear, concise commit messages following the [Conventional Commits](https://www.conventionalcommits.org/) standard. Example:

     ```git
     feat: add support for automatic tax calculation
     ```

2. **Testing**:

   - Before submitting your code, ensure all tests pass:

     ```bash
     make test
     ```

   - If you add new features, please write tests for them using pytest.
   - Run the complete check to ensure code quality:

     ```bash
     make check
     ```

3. **Documentation**:
   - Update or add documentation in the relevant areas.
   - Add appropriate type hints to new functions and classes.
   - Ensure that docstrings are clear and follow the project standards.

## Submitting Changes

1. **Push to Your Fork**:

   - Push your branch to your forked repository:

     ```bash
     git push origin feature/your-feature-name
     ```

2. **Create a Pull Request (PR)**:

   - Go to the Pull Requests section of the original repository.
   - Click "New Pull Request".
   - Select your branch and provide a clear, descriptive title and a summary of your changes.
   - Reference any related issues by including "Fixes #issue_number" in the description.

3. **Review Process**:
   - A project maintainer will review your PR and may ask for changes.
   - Once your PR is approved, it will be merged into the main branch.
   - Please be patient during the review process and be open to feedback.

## Reporting Issues

- If you encounter a bug or have a feature request, please open an issue.
- Provide as much information as possible, including steps to reproduce the issue, environment details, and any other relevant information.
- Use issue templates if available.

## Pull Request Guidelines

- Keep your PR focused on a single feature or fix.
- Maintain the project's coding style.
- Ensure all automated checks pass.
- Update documentation for significant changes.
- Add appropriate tests.
- Rebase your branch before submitting the PR if there have been changes to the main branch.

Thank you for contributing! Your help makes nimara-stripe better for everyone.
