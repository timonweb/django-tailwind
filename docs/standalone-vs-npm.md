# Standalone vs npm-based installation

Django Tailwind offers two methods for integrating Tailwind CSS into your Django project: using an npm-based setup or a
standalone binary. Each method has its own advantages and trade-offs. The table below compares the two approaches to help
you decide which one is best suited for your needs.

| Feature              | npm-based                 | Standalone Binary     |
|----------------------|---------------------------|-----------------------|
| **Node.js Required** | ✅ Yes (22+)               | ❌ No                  |
| **Setup Complexity** | Moderate                  | Simple                |
| **Tailwind Version** | v4 (v3 deprecated)        | v4 only               |
| **Plugin Support**   | ✅ Full                    | ⚠️ DaisyUI only        |
| **DaisyUI Support**  | ✅ Yes                     | ✅ Yes                 |
| **Custom PostCSS**   | ✅ Yes                     | ❌ No                  |
| **Plugin Install**   | `tailwind plugin_install` | `plugin_install daisyui` only |
| **package.json**     | ✅ Created                 | ❌ Not created         |
| **node_modules**     | ✅ Created                 | ❌ Not created         |
| **Best For**         | Teams, complex projects   | Solo, simple projects |

**Choose npm-based if you:**
- Need Tailwind plugins other than DaisyUI
- Want to customize PostCSS configuration
- Prefer managing dependencies with package.json
- Need the plugin management commands

**Choose standalone binary if you:**
- Want the simplest possible setup
- Don't have or don't want to install Node.js
- Don't need plugins beyond DaisyUI, or advanced customization
- Are building a basic project with core Tailwind features
