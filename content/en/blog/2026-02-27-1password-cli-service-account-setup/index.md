---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "Setting Up Non-Interactive Authentication for 1Password CLI with a Service Account"
subtitle: ""
summary: "Notes on the setup procedure for using 1Password CLI (the op command) non-interactively in scripts and automation environments via a Service Account. Covers the full flow from creating a dedicated Vault and obtaining a token, setting it in environment variables, and verifying operation with op read / op inject / op run."
tags: ["1Password"]
categories: ["その他"]
url: 1password-cli-service-account-setup
date: 2026-02-27
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: fals
---

## Introduction

1Password CLI (the `op` command) is a tool for managing 1Password items from the terminal. Specifically, it enables the following:

- **Retrieving secrets**: Safely referencing API keys and DB passwords within scripts
- **Injecting environment variables**: Writing Secret References in `.env` files and replacing them with actual values at runtime
- **Expanding templates**: Embedding 1Password values into configuration file templates for output
- **Managing items**: Creating, updating, and deleting login credentials and secure notes from the CLI

Normally, Touch ID or master password input is required on every execution, which becomes a barrier in non-interactive environments such as automation scripts or CI/CD pipelines.

Using [1Password Service Accounts](https://developer.1password.com/docs/service-accounts/), you can run `op` commands without interactive operations via token-based authentication. This article documents the procedure from creating a Service Account to configuring CLI integration.

## Authentication Method Comparison

1Password CLI has three main authentication methods:

| Method | Interactive operations | Use case | Private Vault |
|--------|----------------------|---------|---------------|
| `op signin` (password) | Required every time | Manual operations | Accessible |
| Touch ID integration | Touch ID required | Desktop environments | Accessible |
| Service Account | Not required | Scripts/automation | Not accessible |

Service Accounts complete authentication simply by setting the token in an environment variable, making them well-suited for use from scripts. However, there is a constraint that Private Vault (personal vault) is not accessible. CLI version 2.18.0 or later is required.

## Service Account Creation Procedure

### Prerequisite: Creating a Dedicated Vault

Since Service Accounts cannot access Private Vaults, create a Vault for CLI use in advance.

1. Sign in to [my.1password.com](https://my.1password.com)
2. Click "Vaults" in the left sidebar
3. Create a new vault with any name (e.g., `Vault`) via "+ New Vault"

### Creating the Service Account

1. Click "Developer" in the left sidebar
2. Select "Infrastructure Secrets" → "Service Accounts"
3. Click "Create a Service Account"
4. Enter a name for the service account (e.g., `cli-automation`)
5. Under "Select vaults," select the Vault you just created and configure permissions (read / read-write)
6. Configure "Environment access" (the default is fine)
7. A token is displayed—copy it immediately and store it somewhere safe

The token is displayed only once at creation. It cannot be displayed again after closing the screen, so be careful.

## Token Configuration

Set the obtained token as the `OP_SERVICE_ACCOUNT_TOKEN` environment variable.

```bash
# Add to .zshrc
echo 'export OP_SERVICE_ACCOUNT_TOKEN="ops_xxxxxxxxxxxxxxxxx"' >> ~/.zshrc

# Apply to current shell
source ~/.zshrc
```

If `OP_CONNECT_HOST` and `OP_CONNECT_TOKEN` are set, they take precedence over `OP_SERVICE_ACCOUNT_TOKEN`, so remove or comment them out if not needed.

## Verification

Verify the configuration is correct.

```bash
# List accessible Vaults
op vault list
```

Example output:

```
ID                            NAME
xxxxxxxxxxxxxxxxxxxxxxxx      Vault
```

Also verify item operations.

```bash
# Check item list
op item list --vault "Vault"

# Create a test login item
op item create --category login \
  --title "Test Item" \
  --vault "Vault" \
  --url "https://example.com" \
  --generate-password

# Display details of a specific item
op item get "Test Item" --vault "Vault"

# Get only the password field of an item
op item get "Test Item" --vault "Vault" --fields password

# Create a secure note
op item create --category "Secure Note" \
  --title "API Config Note" \
  --vault "Vault"

# Delete an item
op item delete "Test Item" --vault "Vault"
```

Using `op read`, you can directly retrieve an item field in Secret Reference format. Convenient for use in shell scripts.

```bash
# Get password in Secret Reference format
op read "op://Vault/Test Item/password"

# Example of assigning to environment variable
export DB_PASSWORD=$(op read "op://Vault/db-credentials/password")
```

Using `op inject`, you can replace placeholders in template files with 1Password values.

```bash
# Template example (config.tpl)
# DATABASE_URL=postgres://user:{{ op://Vault/db-credentials/password }}@localhost/mydb

op inject -i config.tpl -o config.env
```

Using `op run`, you can execute commands with environment variables injected from 1Password.

```bash
# Resolve Secret References in .env file and execute
# .env content: API_KEY=op://Vault/api-key/credential
op run --env-file=.env -- python app.py
```

If any of these commands complete without displaying a password input or Touch ID prompt, the configuration is successful.

## Summary

- Using 1Password CLI's Service Account enables token-based non-interactive authentication
- Since Private Vaults are not accessible, a dedicated Vault needs to be created
- Usage can begin simply by setting the token in the `OP_SERVICE_ACCOUNT_TOKEN` environment variable

## References

{{< linkcard "https://developer.1password.com/docs/service-accounts/" >}}

{{< linkcard "https://developer.1password.com/docs/service-accounts/get-started/" >}}

{{< linkcard "https://developer.1password.com/docs/service-accounts/use-with-1password-cli/" >}}
