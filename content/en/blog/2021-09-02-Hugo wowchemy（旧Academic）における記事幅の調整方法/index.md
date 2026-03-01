---
# Documentation: https://sourcethemes.com/academic/docs/managing-content/

title: "How to Adjust Article Width in Hugo Wowchemy (formerly Academic)"
subtitle: ""
summary: " "
tags: ["Hugo"]
categories: ["Hugo"]
url: hugo-wowchemy-academic-article-container
date: 2021-09-02
featured: false
draft: false

# Featured image
# To use, add an image named `featured.jpg/png` to your pages folder.
# Focal points: Smart, Center, TopLeft, Top, TopRight, Left, Right, BottomLeft, Bottom, BottomRight.
image:
  caption: ""
  focal_point: ""
  preview_only: f
---



Customization can be done as follows.

For advanced style customization, you can write CSS code to override or enhance existing styles.

1. Create the `assets/scss/` folder if it doesn't exist.
2. Create a file named `custom.scss` in the `assets/scss/` folder.
3. Add your custom CSS code to the file you created and re-run Hugo to view the changes.

You can specify it like this as appropriate:

```
.article-container {
    width: 100%;
    max-width: 1000px;
    min-width: 500px;
    margin-right: auto;
    margin-left: auto;
}
```

Reference

[Extending Wowchemy \| Wowchemy: Free, No Code Website Builder for Hugo themes](https://wowchemy.com/docs/guide/extending-wowchemy/)

> ##### Customize style (CSS)
>
> To personalize Wowchemy, you can **choose a colour theme and font set** in `config/_default/params.yaml`.
>
> For further personalization, you can [**create your own colour theme and font theme**](https://wowchemy.com/docs/getting-started/customization/#custom-theme).
>
> If advanced style customization is required, **CSS code** can be written to override or enhance the existing styles:
>
> 1. Create the `assets/scss/` folder if it doesn't exist
> 2. Create a file named `custom.scss` in the `assets/scss/` folder
> 3. Add your custom CSS code to the file you created and re-run Hugo to view changes
