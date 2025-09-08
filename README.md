# Document Summarizer

A modern web application that uses OCR (Optical Character Recognition) and AI to extract and summarize text from uploaded documents. Built with React frontend and Flask backend, featuring Tesseract OCR and optional DeepSeek AI integration.

## 🚀 Features

- **Document Upload**: Support for PDF, JPG, PNG, TIFF image formats
- **OCR Text Extraction**: Uses Tesseract OCR to extract text from images
- **AI-Powered Summarization**: Optional DeepSeek AI integration for intelligent document summarization
- **Modern UI**: Clean, responsive React interface with Material-UI components
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **File Processing**: Automatic image validation and processing

## 🏗️ Tech Stack

### Frontend

- **React 19.1.1** - Modern React with latest features
- **Vite 7.1.2** - Fast build tool and development server
- **Material-UI 7.3.1** - Modern UI components
- **Axios 1.11.0** - HTTP client for API communication
- **React Router DOM 7.8.0** - Client-side routing

### Backend

- **Flask 3.0.3** - Lightweight Python web framework
- **Pillow 10.4.0** - Python Imaging Library for image processing
- **Pytesseract 0.3.13** - Python wrapper for Tesseract OCR
- **OpenAI 1.40.0** - DeepSeek AI integration
- **Flask-CORS 4.0.1** - Cross-Origin Resource Sharing support

## 📁 Project Structure

```
Minor1/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # API endpoints
│   │   ├── core/
│   │   │   └── config.py          # Configuration settings
│   │   ├── services/
│   │   │   ├── extract.py         # AI summarization logic
│   │   │   ├── images.py          # Image processing utilities
│   │   │   └── ocr.py             # OCR text extraction
│   │   └── main.py                # Flask application entry point
│   ├── requirements.txt           # Python dependencies
│   ├── env.example               # Environment variables template
│   └── uploads/                  # Uploaded files directory
├── frontend/
│   ├── src/
│   │   ├── api/
│   │   │   └── axios.js          # API configuration
│   │   ├── pages/
│   │   │   └── Upload.jsx         # Upload page component
│   │   ├── App.jsx               # Main application component
│   │   ├── App.css               # Application styles
│   │   ├── index.css             # Global styles
│   │   └── main.jsx              # Application entry point
│   ├── package.json              # Node.js dependencies
│   ├── vite.config.js            # Vite configuration
│   └── eslint.config.js          # ESLint configuration
├── .gitignore                    # Git ignore rules
└── README.md                     # This file
```

## 🛠️ Installation & Setup

### Prerequisites

- **Python 3.11+** (for backend)
- **Node.js 20+** (for frontend)
- **Tesseract OCR** (for text extraction)
  - **Windows**: Install from [UB Mannheim](https://github.com/UB-Mannheim/tesseract/wiki) or use `winget install UB-Mannheim.TesseractOCR`
  - **macOS**: `brew install tesseract`
  - **Ubuntu/Debian**: `sudo apt-get install -y tesseract-ocr libgl1`

### Quick Start (Local Development)

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd Minor1
   ```

2. **Setup Backend**

   ```bash
   cd backend
   python -m venv .venv

   # Windows PowerShell
   .\.venv\Scripts\Activate.ps1

   # macOS/Linux
   source .venv/bin/activate

   pip install -r requirements.txt
   ```

3. **Configure Environment Variables**

   ```bash
   # Copy the example environment file
   cp env.example .env

   # Edit .env and add your DeepSeek API key (optional)
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   UPLOAD_DIR=./uploads
   OCR_ENGINE=tesseract
   CORS_ORIGIN=*
   ```

4. **Start Backend Server**

   ```bash
   python -m app.main
   # Server runs at http://localhost:5000
   ```

5. **Setup Frontend** (in a new terminal)

   ```bash
   cd frontend
   npm install
   npm run dev
   # Frontend runs at http://localhost:5173
   ```

6. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend Health Check: http://localhost:5000/health

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the backend directory:

```env
# DeepSeek API Configuration (optional)
DEEPSEEK_API_KEY=your_deepseek_api_key_here

# File Upload Settings
UPLOAD_DIR=./uploads

# OCR Engine Selection
OCR_ENGINE=tesseract

# CORS Settings
CORS_ORIGIN=*
```

### DeepSeek AI Integration (Optional)

To enable AI-powered document summarization:

1. Get a DeepSeek API key from [DeepSeek](https://platform.deepseek.com/)
2. Add it to your `.env` file:
   ```env
   DEEPSEEK_API_KEY=your_actual_api_key_here
   ```
3. Restart the backend server

Without the API key, the application will use simple text-based summarization.

## 📡 API Endpoints

### Base URL: `http://localhost:5000/api/v1`

| Method | Endpoint     | Description                     | Request Body                            |
| ------ | ------------ | ------------------------------- | --------------------------------------- |
| `POST` | `/summarize` | Upload and summarize a document | `multipart/form-data` with `file` field |
| `GET`  | `/health`    | Health check endpoint           | None                                    |

### Example API Usage

**Upload Document (PowerShell)**

```powershell
$form = @{ file = Get-Item 'C:\path\to\document.jpg' }
Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://localhost:5000/api/v1/summarize -Form $form
```

**Upload Document (curl)**

```bash
curl -X POST -F "file=@document.jpg" http://localhost:5000/api/v1/summarize
```

### Response Format

```json
{
  "file_type": "image",
  "summary": "Document contains information about...",
  "extracted_text_length": 1234,
  "processed_at": "2024-01-01T12:00:00.000Z"
}
```

## 🎯 Usage

1. **Open the Application**: Navigate to http://localhost:5173
2. **Upload Document**: Click "Choose File" and select a supported document (PDF, JPG, PNG, TIFF)
3. **Process**: Click "Summarize Document" to extract text and generate summary
4. **View Results**: The application will display:
   - AI-generated summary (if DeepSeek API is configured)
   - File type information
   - Extracted text length
   - Processing timestamp

## 🔍 Supported File Types

- **Images**: JPG, JPEG, PNG, TIFF, TIF
- **Documents**: PDF (basic support)

## 🐛 Troubleshooting

### Common Issues

**1. Tesseract Not Found**

```
Error: Tesseract OCR is not installed
```

- **Solution**: Install Tesseract OCR and ensure it's in your system PATH
- **Windows**: Download from UB Mannheim or use `winget install UB-Mannheim.TesseractOCR`
- **macOS**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`

**2. CORS Issues**

```
Access to fetch at 'http://localhost:5000' from origin 'http://localhost:5173' has been blocked by CORS policy
```

- **Solution**: Ensure `CORS_ORIGIN` is set to `*` or your frontend URL in `.env`

**3. File Upload Errors**

```
Error: Invalid file type
```

- **Solution**: Ensure you're uploading supported file types (PDF, JPG, PNG, TIFF)

**4. DeepSeek API Errors**

```
Error: DeepSeek summary failed
```

- **Solution**: Check your API key in `.env` or remove it to use simple summarization

### Debug Mode

To enable debug logging, modify `backend/app/main.py`:

```python
app.run(host="0.0.0.0", port=5000, debug=True)
```

## 🚀 Development

### Backend Development

```bash
cd backend
python -m app.main
```

### Frontend Development

```bash
cd frontend
npm run dev
```

### Building for Production

**Frontend**

```bash
cd frontend
npm run build
```

**Backend**

```bash
cd backend
pip install -r requirements.txt
python -m app.main
```

## 📝 Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Commit changes: `git commit -am 'Add feature'`
4. Push to branch: `git push origin feature-name`
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Support

For support and questions:

- Create an issue in the repository
- Check the troubleshooting section above
- Ensure all prerequisites are installed correctly

## 🔧 Development Configuration

### ESLint Configuration

The project uses ESLint for code quality. To expand the ESLint configuration for production applications, you can enable type-aware lint rules:

```js
export default tseslint.config([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Other configs...
      ...tseslint.configs.recommendedTypeChecked,
      // Alternatively, use this for stricter rules
      ...tseslint.configs.strictTypeChecked,
      // Optionally, add this for stylistic rules
      ...tseslint.configs.stylisticTypeChecked,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
]);
```

### React-Specific Linting

For enhanced React development, you can install additional ESLint plugins:

```bash
npm install --save-dev eslint-plugin-react-x eslint-plugin-react-dom
```

Then update your `eslint.config.js`:

```js
import reactX from "eslint-plugin-react-x";
import reactDom from "eslint-plugin-react-dom";

export default tseslint.config([
  globalIgnores(["dist"]),
  {
    files: ["**/*.{ts,tsx}"],
    extends: [
      // Enable lint rules for React
      reactX.configs["recommended-typescript"],
      // Enable lint rules for React DOM
      reactDom.configs.recommended,
    ],
    languageOptions: {
      parserOptions: {
        project: ["./tsconfig.node.json", "./tsconfig.app.json"],
        tsconfigRootDir: import.meta.dirname,
      },
    },
  },
]);
```

### Vite Configuration

The project uses Vite for fast development and building. Key features:

- **Hot Module Replacement (HMR)** for instant updates during development
- **Fast Refresh** for React components
- **Optimized builds** for production

Available Vite plugins:

- `@vitejs/plugin-react` - Uses Babel for Fast Refresh
- `@vitejs/plugin-react-swc` - Uses SWC for even faster refresh (alternative)

## 🔮 Future Enhancements

- [ ] Docker containerization
- [ ] Database integration for storing processed documents
- [ ] Batch processing capabilities
- [ ] Enhanced PDF processing
- [ ] Multiple OCR engine support (EasyOCR)
- [ ] User authentication and document management
- [ ] Advanced AI models integration
- [ ] Document classification and categorization
- [ ] TypeScript migration for better type safety
- [ ] Enhanced ESLint configuration with React-specific rules
- [ ] Unit and integration testing setup
- [ ] CI/CD pipeline configuration

## 📚 Additional Resources

### React + Vite Template Information

This project is built on the React + Vite template, which provides:

- Minimal setup for React development
- ESLint rules for code quality
- Hot Module Replacement (HMR)
- Fast build times with Vite

### Development Tools

- **ESLint**: Code linting and formatting
- **Vite**: Build tool and development server
- **Material-UI**: Component library
- **Axios**: HTTP client
- **React Router**: Client-side routing

---

**Note**: This application is designed for educational and development purposes. Ensure you have proper permissions before processing sensitive documents.
