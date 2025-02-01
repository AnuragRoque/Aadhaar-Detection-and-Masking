# Aadhaar Detection and Masking

This project provides three versions of Aadhaar number detection and masking for scanned or digital copies of documents. These versions offer varying levels of complexity, efficiency, and additional features. Choose the version based on your requirements.

## Algorithm Overview

* Utilizes **ISR.models RRDN** for image enhancement and **pytesseract** for Aadhaar UID recognition.
* Supports masking for 5+ Aadhaar formats with the ability to handle 1-3 UIDs in images.
* Future improvements include  **OpenCV contour detection** ,  **adaptive thresholding** , and **noise reduction** ( **cv2.fastNlMeansDenoising** ).
* Processes files from S3, checks if Aadhaar UID is present, and applies masking.
* Updates a CSV with document type, UID status, and number of times masking is applied.
* Automatically retries masking until all UIDs are masked or found.
* Deletes processed documents after completion and moves to the next document.

## Versions Overview

### **v1 - Simple Single File Aadhaar Detection and Masking**

This version is designed for simple, one-time processing of Aadhaar numbers in a single document. It offers a straightforward solution for Aadhaar detection and masking with basic functionality.

- **Features:**

  - Processes a single file at a time.
  - Basic Aadhaar number detection and masking.
  - Simple and easy to implement.
- **Pros:**

  - Easy to set up and use.
  - Ideal for small tasks or one-off processing.
  - Low system resource usage.
- **Cons:**

  - Not suitable for processing large numbers of files.
  - Limited error handling and reporting.
  - No support for output file tracking or logging.

---

### **v2 - More Efficient Aadhaar Detection and Masking**

This version improves upon the first by introducing more efficient processing methods for handling multiple files. It is more suitable for scenarios where a larger batch of documents needs to be processed.

- **Features:**

  - Processes multiple files efficiently in batch mode.
  - Optimized for faster Aadhaar number detection and masking.
  - Includes basic error handling.
- **Pros:**

  - Faster processing compared to v1.
  - Suitable for batch processing.
  - Improved resource management for multiple files.
- **Cons:**

  - Lacks file tracking or status management.
  - Minimal error reporting.
  - Limited scalability for very large datasets.

---

### **v3 - Advanced Aadhaar Detection and Masking with Sheet Status**

This is the most advanced version, designed for large-scale operations that require not only Aadhaar detection and masking but also file tracking and status reporting in an Excel sheet. It’s ideal for enterprises or organizations handling numerous files with detailed status tracking.

- **Features:**

  - Advanced masking techniques.
  - Supports batch processing of multiple files.
  - Tracks the status of each processed file in an Excel sheet.
  - Excellent error handling with detailed logging and reporting.
- **Pros:**

  - Best for large-scale operations with numerous files.
  - Provides detailed status tracking in an Excel sheet.
  - Robust error handling and reporting.
  - High scalability for enterprise-level use.
- **Cons:**

  - Requires more system resources due to Excel integration and batch processing.
  - More complex setup and usage compared to v1 and v2.

---

## Requirements

Before running any of the versions, ensure you have the following dependencies installed:

Dependencies:

```bash
pip install numpy opencv-python pillow pytesseract pdf2image img2pdf PyPDF2 tifftools openpyxl regex
```

```bash
pip install numpy opencv-python pillow pytesseract pdf2image img2pdf PyPDF2 tifftools openpyxl regex
```

 **Libraries and Packages** :

Python Version: 3.7.9

* `numpy`
* `pytesseract`
* `opencv-python`
* `Pillow` (Python Imaging Library)
* `pdf2image`
* `img2pdf`
* `PyPDF2`
* `tifftools`
* `openpyxl`
* `ISR` (for image super-resolution in v3)
* `regex` (for regular expressions)
* `tkinter` (for GUI interface)

## Features Comparison

| Feature                          | Code v1 - Simple Single File | Code v2 - More Efficient        | Code v3 - With Sheet Status                                 |
| -------------------------------- | ---------------------------- | ------------------------------- | ----------------------------------------------------------- |
| **Batch Processing**       | ❌ (one file at a time)      | ✔ (multiple files efficiently) | ✔ (multiple files with advanced status tracking)           |
| **Efficiency**             | ❌ (basic, can be slow)      | ✔ (improved efficiency)        | ✔ (high efficiency with advanced techniques)               |
| **Error Handling**         | ❌ (minimal error reporting) | ✔ (better error handling)      | ✔ (excellent error handling with detailed reporting)       |
| **Output File Tracking**   | ❌ (no tracking mechanism)   | ❌ (no tracking)                | ✔ (output tracked in Excel sheet)                          |
| **Logging**                | ❌ (no tracking progress)    | ❌ (minimal logging)            | ✔ (tracks status in Excel)                                 |
| **Scalability**            | ❌ (limited scalability)     | ✔ (more scalable)              | ✔ (most scalable with robust tracking)                     |
| **File Management**        | ❌ (handles single file)     | ✔ (handles multiple files)     | ✔ (advanced file handling with status updates)             |
| **Integration with Excel** | ❌ (no integration)          | ❌ (no integration)             | ✔ (integrates Excel for status tracking)                   |
| **Complexity**             | ✔ (simple to understand)    | ✔ (moderately complex)         | ❌ (complex, requires understanding of multiple components) |
| **System Resource Usage**  | ✔ (low resources required)  | ✔ (moderate resource usage)    | ❌ (high resource usage)                                    |
| **Best For**               | ✔ (small, simple tasks)     | ✔ (medium-scale tasks)         | ❌ (large-scale operations with reporting)                  |

## Troubleshooting

* **Error Handling:** All versions have some level of error handling, but if issues arise (e.g., incorrect file format), check the logs or console output for error messages.
* **Missing Dependencies:** Make sure all required libraries and external tools are installed. See the Requirements section for more details.

---

## License

This project is licensed under the MIT License - see the [LICENSE]() file for details.

## Developed By Anurag Roque

Contract me for help and guide
[Anurag Singh](mailto:anuragsingh2445@gmail.com) 📧 anuragsingh2445@gmail.com
