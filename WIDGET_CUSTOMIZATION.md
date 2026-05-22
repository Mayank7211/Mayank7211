# Widget Customization Guide

## Theme Configuration

The widget can be fully customized to match your brand and website design. Pass customization parameters via data attributes on the script tag.

---

## Basic Customization

### Default (No customization):
```html
<script src="https://yourdomain.com/widget/agent.js" data-tenant-id="YOUR_TENANT_ID"></script>
```

---

## Full Customization Example:

```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="YOUR_TENANT_ID"
  data-theme-primary="#667eea"
  data-theme-accent="#764ba2"
  data-background="#ffffff"
  data-text-color="#333333"
  data-header-text="Chat with our team"
  data-placeholder="Ask a question..."
  data-logo-url="https://yourcompany.com/logo.png"
  data-button-position="bottom-right"
  data-button-size="60"
  data-width="400"
  data-height="600"
></script>
```

---

## Customization Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `data-tenant-id` | String | Required | Your business tenant ID (from onboarding) |
| `data-theme-primary` | HEX Color | #667eea | Primary color for buttons, gradients |
| `data-theme-accent` | HEX Color | #764ba2 | Accent color for gradients |
| `data-background` | HEX Color | #ffffff | Chat window background color |
| `data-text-color` | HEX Color | #333333 | Default text color |
| `data-header-text` | String | Chat with us | Header title text |
| `data-placeholder` | String | Type your message... | Input field placeholder |
| `data-logo-url` | URL | (empty) | Your logo image URL |
| `data-button-position` | String | bottom-right | Position: bottom-right, bottom-left, top-right, top-left |
| `data-button-size` | Number | 60 | Button diameter in pixels |
| `data-width` | Number | 400 | Chat window width in pixels |
| `data-height` | Number | 600 | Chat window height in pixels |

---

## Color Scheme Examples

### Modern Blue (Default):
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#667eea"
  data-theme-accent="#764ba2"
></script>
```

### Professional Purple:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#9333EA"
  data-theme-accent="#C026D3"
></script>
```

### Healthcare Blue:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#0369A1"
  data-theme-accent="#06B6D4"
></script>
```

### Medical Green:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#16A34A"
  data-theme-accent="#22C55E"
></script>
```

### Luxury Gold:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#B45309"
  data-theme-accent="#F59E0B"
  data-background="#FFFBEB"
></script>
```

### Dark Mode (for dark websites):
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#60A5FA"
  data-theme-accent="#93C5FD"
  data-background="#1F2937"
  data-text-color="#F3F4F6"
></script>
```

---

## Button Position Examples

### Bottom-Right (Default):
```html
<script src="..." data-button-position="bottom-right"></script>
```

### Bottom-Left:
```html
<script src="..." data-button-position="bottom-left"></script>
```

### Top-Right:
```html
<script src="..." data-button-position="top-right"></script>
```

### Top-Left:
```html
<script src="..." data-button-position="top-left"></script>
```

---

## Responsive Behavior

The widget automatically adapts to all screen sizes:

- **Desktop (≥768px)**: Shows chat as floating window with configured dimensions
- **Tablet (480px - 768px)**: Adjusted padding and font sizes for touch
- **Mobile (< 480px)**: Full-screen immersive chat experience
- **Landscape**: Optimized height for landscape orientation
- **Dark Mode**: Automatically detects OS dark mode preference

No additional configuration needed - it's automatic!

---

## Logo/Branding

To add your company logo to the chat header:

```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-logo-url="https://yourcompany.com/logo.png"
></script>
```

**Logo Requirements:**
- Format: PNG, JPG, or SVG
- Size: 40x40 pixels (will be scaled)
- Color: Should contrast with your primary color
- Recommendation: Use a square logo or icon

---

## Size Customization

### Compact Chat:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-width="350"
  data-height="500"
  data-button-size="50"
></script>
```

### Large Chat:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-width="500"
  data-height="700"
  data-button-size="70"
></script>
```

### Mobile Optimized:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-width="400"
  data-height="550"
></script>
```

---

## Language/Text Customization

### English (Default):
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-header-text="Chat with us"
  data-placeholder="Type your message..."
></script>
```

### Spanish:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-header-text="Chatea con nosotros"
  data-placeholder="Escribe tu mensaje..."
></script>
```

### French:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-header-text="Discutez avec nous"
  data-placeholder="Écrivez votre message..."
></script>
```

### Hindi:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-header-text="हमसे बात करें"
  data-placeholder="अपना संदेश टाइप करें..."
></script>
```

---

## Real-World Examples

### Medical Clinic Website:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#0369A1"
  data-theme-accent="#06B6D4"
  data-header-text="Medical Assistant"
  data-placeholder="Describe your symptoms..."
  data-logo-url="https://clinic.com/medical-logo.png"
  data-button-position="bottom-right"
></script>
```

### Beauty Salon Website:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#EC4899"
  data-theme-accent="#F472B6"
  data-background="#FDF2F8"
  data-header-text="Book Your Appointment"
  data-placeholder="When would you like to visit?"
  data-logo-url="https://salon.com/logo.png"
  data-button-size="65"
></script>
```

### Law Firm Website:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#1E3A8A"
  data-theme-accent="#3B82F6"
  data-background="#F8FAFC"
  data-text-color="#1E293B"
  data-header-text="Legal Consultation"
  data-placeholder="Describe your case..."
  data-logo-url="https://lawfirm.com/seal.png"
></script>
```

### Tech Startup Website:
```html
<script
  src="https://yourdomain.com/widget/agent.js"
  data-tenant-id="xyz"
  data-theme-primary="#00D9FF"
  data-theme-accent="#0099FF"
  data-background="#0F172A"
  data-text-color="#E2E8F0"
  data-header-text="AI Support"
  data-button-position="bottom-left"
></script>
```

---

## Mobile Testing

Test your widget on:
- ✅ iPhone (375px width)
- ✅ iPad (768px width)
- ✅ Android phones (360-412px width)
- ✅ Tablets (1024px width)
- ✅ Landscape orientation

The widget automatically optimizes for all these scenarios with no extra configuration.

---

## Accessibility

The widget includes:
- ✅ ARIA labels for screen readers
- ✅ Keyboard navigation support
- ✅ High contrast colors
- ✅ Focus indicators
- ✅ Semantic HTML

---

## Troubleshooting

**Widget not showing?**
- Check that `data-tenant-id` is correct
- Verify `src` URL is correct
- Check browser console for errors
- Ensure backend API is running

**Colors not applying?**
- Use valid HEX color codes (#RRGGBB)
- Check for typos in parameter names
- Clear browser cache and reload

**Mobile issues?**
- Widget auto-resizes - no special config needed
- Test on actual devices, not just browser emulation
- Check viewport meta tag exists: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

**Performance?**
- Widget is lightweight (~15KB)
- Loads asynchronously
- Won't block page loading
- Safe to add multiple instances (not recommended)

---

## Pro Tips

1. **Color Matching**: Use a color picker from your website to match exactly
2. **Logo Quality**: Use SVG for crisp logo appearance
3. **Dark Mode**: Provide both light and dark mode options
4. **Testing**: Test customizations in multiple browsers before going live
5. **Branding**: Keep header text short (< 20 characters) for mobile
6. **Button Size**: Use 50-70px for best feel on different devices
