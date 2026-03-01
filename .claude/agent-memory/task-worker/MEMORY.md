# Task Worker Memory - zatoima.github.io

## Project Structure
- Hugo static site with multilingual support (ja default, en secondary)
- Content: content/ja/ (Japanese), content/en/ (English)
- Layouts: layouts/_default/, layouts/partials/
- Build: `hugo --config hugo.toml -d docs`
- Theme: hugo-bearblog (themes/hugo-bearblog/)

## Key Patterns

### Hugo JSON-LD Template
- Use `"{{ .Language.Lang }}"` (plain string interpolation) NOT `{{ .Language.Lang | jsonify }}`
- `jsonify` on a string like "ja" produces `"ja"` which then becomes `"\"ja\""` when embedded in JSON-LD template

### Hugo Render Link Override
- Created `layouts/_markup/render-link.html` to handle malformed URLs in content
- Use `safeURL` instead of `urls.Parse` to avoid errors on percent-encoded URLs like `%2F`
- Template: `<a href="{{ .Destination | safeURL }}"{{ with .Title }} title="{{ . }}"{{ end }}{{ if strings.HasPrefix .Destination "http" }} target="_blank" rel="noopener noreferrer"{{ end }}>{{ .Text | safeHTML }}</a>`

### Hreflang
- Already added to layouts/_default/baseof.html (lines 30-35)
- Do NOT duplicate in seo_tags.html

### Build Verification
- Test build to /tmp/ before committing: `hugo --config hugo.toml -d /tmp/hugo-i18n-test`
- Raw HTML warnings are non-fatal (many content files have HTML)
- Build errors (exit code 1) must be fixed before deploying
