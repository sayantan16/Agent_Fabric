# Agentic Fabric Registry Report
Generated: 2025-09-03 08:05:21

## System Health
- **Health Score**: 100.0/100
- **Status**: HEALTHY
- **Total Components**: 15
- **Valid Components**: 15

## Registered Agents
### email_extractor
- **Description**: Extracts email addresses from provided text
- **Tools Used**: extract_emails
- **Executions**: 3
- **Lines**: 41

### text_analyzer
- **Description**: Analyze text to extract emails and numbers
- **Tools Used**: extract_emails, extract_numbers
- **Executions**: 0
- **Lines**: 61

### statistics_calculator
- **Description**: Calculate statistics from numbers in text
- **Tools Used**: extract_numbers, calculate_mean, calculate_median
- **Executions**: 2
- **Lines**: 86

### csv_analyzer
- **Description**: Analyze CSV data to extract statistics and create summaries
- **Tools Used**: read_csv, extract_numbers, calculate_mean, calculate_median
- **Executions**: 0
- **Lines**: 78

### document_processor
- **Description**: Process text documents to extract key information
- **Tools Used**: read_text, extract_emails, extract_urls, extract_numbers
- **Executions**: 0
- **Lines**: 69

### pdf_email_extractor
- **Description**: Extract email addresses from PDF documents
- **Tools Used**: read_pdf, extract_emails
- **Executions**: 0
- **Lines**: 68

## Registered Tools
### extract_emails
- **Description**: Extracts email addresses from text using regex
- **Used By**: email_extractor, text_analyzer, document_processor, pdf_email_extractor
- **Lines**: 6

### read_pdf
- **Description**: Extracts text content from PDF files using PyPDF2
- **Used By**: pdf_email_extractor
- **Lines**: 32

### read_csv
- **Description**: Reads CSV files into structured data using pandas
- **Used By**: csv_analyzer
- **Lines**: 22

### read_json
- **Description**: Parses JSON files into Python objects
- **Used By**: None
- **Lines**: 21

### read_text
- **Description**: Reads plain text files
- **Used By**: document_processor
- **Lines**: 21

### extract_numbers
- **Description**: Extracts all numbers from text, including integers and decimals
- **Used By**: text_analyzer, statistics_calculator, csv_analyzer, document_processor
- **Lines**: 33

### calculate_mean
- **Description**: Calculates the arithmetic mean of a list of numbers
- **Used By**: statistics_calculator, csv_analyzer
- **Lines**: 15

### calculate_median
- **Description**: Calculates the median value of a list of numbers
- **Used By**: statistics_calculator, csv_analyzer
- **Lines**: 24

### extract_urls
- **Description**: Extract all URLs from text
- **Used By**: document_processor
- **Lines**: 20

## Usage Analytics
- **Total Executions**: 5
- **Average Agent Size**: 67.2 lines
- **Average Tool Size**: 21.6 lines
