def extract_phones(input_data=None):
        """Extract phone numbers from text."""
        import re
        
        if input_data is None:
            return []
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = ' '.join(str(v) for v in input_data.values())
            
            # Multiple phone patterns
            patterns = [
                r'\+?1?\s*\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}',  # US format
                r'\(\d{3}\)\s*\d{3}-\d{4}',  # (555) 555-5555
                r'\d{3}-\d{3}-\d{4}',  # 555-555-5555
                r'\d{10}',  # 5555555555
            ]
            
            phones = []
            for pattern in patterns:
                matches = re.findall(pattern, text)
                phones.extend(matches)
            
            # Clean and format
            clean_phones = []
            for phone in phones:
                # Remove non-digits for comparison
                digits = re.sub(r'\D', '', phone)
                if len(digits) >= 10:
                    clean_phones.append(phone)
            
            return list(set(clean_phones))
        except Exception:
            return []
    