def analyze_sentiment(input_data=None):
        """Analyze sentiment of text."""
        
        if input_data is None:
            return {"sentiment": "neutral", "score": 0.0}
        
        try:
            text = str(input_data)
            if isinstance(input_data, dict):
                text = input_data.get('text', input_data.get('content', str(input_data)))
            
            text_lower = text.lower()
            
            # Simple but functional sentiment analysis
            positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 
                            'fantastic', 'love', 'perfect', 'best', 'happy', 'awesome',
                            'brilliant', 'outstanding', 'superior', 'positive', 'success']
            negative_words = ['bad', 'terrible', 'awful', 'horrible', 'hate', 'worst',
                            'poor', 'disappointing', 'failure', 'negative', 'wrong',
                            'broken', 'useless', 'waste', 'angry', 'frustrated']
            
            positive_count = sum(1 for word in positive_words if word in text_lower)
            negative_count = sum(1 for word in negative_words if word in text_lower)
            
            # Calculate score
            if positive_count + negative_count == 0:
                sentiment = "neutral"
                score = 0.0
            else:
                score = (positive_count - negative_count) / (positive_count + negative_count)
                if score > 0.2:
                    sentiment = "positive"
                elif score < -0.2:
                    sentiment = "negative"
                else:
                    sentiment = "neutral"
            
            return {
                "sentiment": sentiment,
                "score": score,
                "positive_words": positive_count,
                "negative_words": negative_count
            }
            
        except Exception:
            return {"sentiment": "neutral", "score": 0.0}
    