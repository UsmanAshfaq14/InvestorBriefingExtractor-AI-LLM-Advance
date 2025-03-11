import json
import csv
import re
import datetime
import io
from collections import Counter

class InvestorBriefingExtractor:
    def __init__(self):
        self.expected_keywords = ["growth", "risk", "innovation", "market", "confidence", 
                                  "investment", "strategic", "opportunity", "challenges", "expansion"]
        
    def validate_data(self, data_str, data_format="json"):
        """
        Validates the input data based on the specified format.
        
        Args:
            data_str (str): The input data string.
            data_format (str): The format of the input data ("json" or "csv").
            
        Returns:
            tuple: (is_valid, records, validation_report, error_messages)
        """
        records = []
        error_messages = []
        
        try:
            if data_format.lower() == "json":
                records = self._parse_json(data_str)
            elif data_format.lower() == "csv":
                records = self._parse_csv(data_str)
            else:
                return False, [], "ERROR: Invalid data format. Please provide data in CSV or JSON format.", []
            
            # Validate each record
            for i, record in enumerate(records, 1):
                # Check for required fields
                missing_fields = []
                for field in ["briefing_id", "date", "briefing_text"]:
                    if field not in record or not record[field]:
                        missing_fields.append(field)
                
                if missing_fields:
                    error_msg = f"ERROR: Missing required field(s): {', '.join(missing_fields)} in record {i}."
                    error_messages.append(error_msg)
                    continue
                
                # Validate date format
                if not self._is_valid_date(record["date"]):
                    error_msg = f"ERROR: Invalid value for the field(s): date in record {i}. Please correct and resubmit."
                    error_messages.append(error_msg)
                
                # Validate key_metrics if provided
                if "key_metrics" in record and record["key_metrics"]:
                    try:
                        key_metrics = float(record["key_metrics"])
                        if key_metrics <= 0:
                            error_msg = f"ERROR: Invalid value for the field(s): key_metrics in record {i}. Must be a positive number."
                            error_messages.append(error_msg)
                    except ValueError:
                        error_msg = f"ERROR: Invalid data type for the field(s): key_metrics in record {i}. Please ensure numeric values."
                        error_messages.append(error_msg)
            
            # Generate validation report
            validation_report = self._generate_validation_report(records, error_messages)
            return len(error_messages) == 0, records, validation_report, error_messages
            
        except Exception as e:
            error_msg = f"ERROR: {str(e)}"
            return False, [], error_msg, [error_msg]
    
    def _parse_json(self, json_str):
        """Parse JSON data and return a list of records."""
        try:
            data = json.loads(json_str)
            if "briefings" in data and isinstance(data["briefings"], list):
                return data["briefings"]
            elif isinstance(data, list):
                return data
            else:
                raise ValueError("Invalid JSON structure. Expected a list of briefings or a 'briefings' field containing a list.")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format. Please check your data.")
    
    def _parse_csv(self, csv_str):
        """Parse CSV data and return a list of records."""
        try:
            records = []
            csv_reader = csv.DictReader(io.StringIO(csv_str))
            for row in csv_reader:
                records.append(dict(row))
            return records
        except Exception:
            raise ValueError("Invalid CSV format. Please check your data.")
    
    def _is_valid_date(self, date_str):
        """Check if the date string is in YYYY-MM-DD format."""
        pattern = r"^\d{4}-\d{2}-\d{2}$"
        if not re.match(pattern, date_str):
            return False
        
        try:
            datetime.datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _generate_validation_report(self, records, error_messages):
        """Generate a validation report in markdown format."""
        report = "# Investor Briefing Data Validation Report\n"
        report += "## Overview\n"
        report += f"- Total Briefings Provided: {len(records)}\n"
        report += "## Field Checks per Record\n"
        
        all_valid = True
        for i, record in enumerate(records, 1):
            report += f"\n### Record {i}\n"
            # Check briefing_id
            briefing_id_status = "**present**" if "briefing_id" in record and record["briefing_id"] else "**missing**"
            report += f"- briefing_id: {briefing_id_status}\n"
            
            # Check date
            date_status = "**valid**" if "date" in record and self._is_valid_date(record["date"]) else "**invalid**"
            report += f"- date: {date_status}\n"
            
            # Check briefing_text
            briefing_text_status = "**present**" if "briefing_text" in record and record["briefing_text"] else "**missing**"
            report += f"- briefing_text: {briefing_text_status}\n"
            
            # Check key_metrics
            key_metrics_status = "**not provided**"
            if "key_metrics" in record and record["key_metrics"]:
                try:
                    key_metrics = float(record["key_metrics"])
                    key_metrics_status = "**valid**" if key_metrics > 0 else "**invalid**"
                except ValueError:
                    key_metrics_status = "**invalid**"
            report += f"- key_metrics: {key_metrics_status}\n"
            
            # Update all_valid flag
            if "**missing**" in [briefing_id_status, briefing_text_status] or "**invalid**" in [date_status, key_metrics_status]:
                all_valid = False
        
        report += "\n## Summary\n"
        if all_valid and not error_messages:
            report += "Data validation is successful! Would you like to proceed with theme extraction?\n"
        else:
            report += "The following errors were found:\n"
            for error in error_messages:
                report += f"- {error}\n"
        
        return report
    
    def process_briefings(self, records):
        """
        Process each briefing record and generate a detailed report.
        
        Args:
            records (list): List of validated briefing records.
            
        Returns:
            str: The formatted final report in markdown.
        """
        results = []
        records_with_key_metrics = [r for r in records if "key_metrics" in r and r["key_metrics"]]
        
        avg_key_metric = 0
        if records_with_key_metrics:
            sum_key_metrics = sum(float(r["key_metrics"]) for r in records_with_key_metrics)
            avg_key_metric = sum_key_metrics / len(records_with_key_metrics)
        
        for record in records:
            # Process each record
            result = self._process_single_briefing(record, avg_key_metric)
            results.append(result)
        
        # Generate the final report
        final_report = self._generate_final_report(results)
        return final_report
    
    def _process_single_briefing(self, record, avg_key_metric):
        """Process a single briefing record and return the analysis results."""
        briefing_id = record["briefing_id"]
        date = record["date"]
        briefing_text = record["briefing_text"]
        key_metrics = float(record["key_metrics"]) if "key_metrics" in record and record["key_metrics"] else None
        
        # Calculate keyword frequencies
        word_count = len(briefing_text.split())
        keyword_counts = Counter()
        
        # Count occurrences of each expected keyword in the text (case-insensitive)
        for keyword in self.expected_keywords:
            pattern = r'\b' + re.escape(keyword) + r'\b'
            matches = re.finditer(pattern, briefing_text.lower())
            count = sum(1 for _ in matches)
            keyword_counts[keyword] = count
        
        # Calculate total keyword frequency
        total_keyword_frequency = sum(keyword_counts.values())
        
        # Calculate Normalized Keyword Score
        normalized_keyword_score = total_keyword_frequency / word_count if word_count > 0 else 0
        
        # Calculate Diversity Score
        unique_keywords_found = sum(1 for keyword, count in keyword_counts.items() if count > 0)
        diversity_score = (unique_keywords_found / len(self.expected_keywords)) * 100
        
        # Calculate Composite Thematic Score
        composite_thematic_score = (normalized_keyword_score * 50) + (diversity_score * 0.5)
        
        # Determine thematic intensity and recommendation
        if composite_thematic_score > 30.00 and normalized_keyword_score > 0.02:
            thematic_intensity = "High"
            recommendation = "Focus on strategic growth and risk mitigation."
        else:
            thematic_intensity = "Moderate"
            recommendation = "Review the investor briefing for additional insights."
        
        # Prepare results dictionary
        result = {
            "briefing_id": briefing_id,
            "date": date,
            "briefing_text_snippet": briefing_text[:100] + "..." if len(briefing_text) > 100 else briefing_text,
            "key_metrics": key_metrics,
            "avg_key_metric": avg_key_metric,
            "keyword_counts": dict(keyword_counts),
            "total_keyword_frequency": total_keyword_frequency,
            "word_count": word_count,
            "normalized_keyword_score": normalized_keyword_score,
            "unique_keywords_found": unique_keywords_found,
            "diversity_score": diversity_score,
            "composite_thematic_score": composite_thematic_score,
            "thematic_intensity": thematic_intensity,
            "recommendation": recommendation
        }
        
        return result
    
    def _generate_final_report(self, results):
        """Generate the final report in markdown format."""
        report = "# Investor Briefing Summary\n"
        report += f"## Total Briefings Evaluated: {len(results)}\n\n"
        report += "### Detailed Analysis per Briefing:\n"
        
        for result in results:
            report += f"#### Briefing {result['briefing_id']}\n"
            report += "**Input Data:**\n"
            report += f"- Date: {result['date']}\n"
            report += f"- Briefing Text Snippet: {result['briefing_text_snippet']}\n"
            
            if result['key_metrics'] is not None:
                report += f"- Key Metrics: {result['key_metrics']:.2f}\n"
            else:
                report += "- Key Metrics: Not provided\n"
            
            report += "\n**Detailed Calculations:**\n"
            
            # 1. Average Key Metric Calculation
            report += "1. **Average Key Metric Calculation:**\n"
            report += " - Formula: $$ \\text{Average Key Metric} = \\frac{\\text{Sum of key\\_metrics}}{\\text{Number of records with key\\_metrics}} $$\n"
            
            if result['key_metrics'] is not None:
                report += f" - Calculation Steps: Sum of key_metrics / Number of records = {result['avg_key_metric']:.2f}\n"
            else:
                report += " - Calculation Steps: No key_metrics provided for this record\n"
            
            report += f" - Result: **{result['avg_key_metric']:.2f}**\n"
            
            # 2. Keyword Frequency Calculation
            report += "2. **Keyword Frequency Calculation:**\n"
            report += f" - Expected Keywords: \"{', '.join(self.expected_keywords)}\"\n"
            report += " - Keyword Occurrences:\n"
            
            for keyword, count in result['keyword_counts'].items():
                report += f"   - \"{keyword}\": {count}\n"
            
            report += f" - Total Keyword Frequency: **{result['total_keyword_frequency']}**\n"
            
            # 3. Normalized Keyword Score Calculation
            report += "3. **Normalized Keyword Score Calculation:**\n"
            report += " - Formula: $$ \\text{Normalized Keyword Score} = \\frac{\\text{Total Keyword Frequency}}{\\text{Total Number of Words}} $$\n"
            report += f" - Calculation Steps: {result['total_keyword_frequency']} / {result['word_count']} = {result['normalized_keyword_score']:.4f}\n"
            report += f" - Result: **{result['normalized_keyword_score']:.4f}**\n"
            
            # 4. Diversity Score Calculation
            report += "4. **Diversity Score Calculation:**\n"
            report += " - Formula: $$ \\text{Diversity Score} = \\frac{\\text{Number of Unique Keywords Found}}{10} \\times 100 $$\n"
            report += f" - Calculation Steps: ({result['unique_keywords_found']} / 10) × 100 = {result['diversity_score']:.2f}%\n"
            report += f" - Result: **{result['diversity_score']:.2f}%**\n"
            
            # 5. Composite Thematic Score Calculation
            report += "5. **Composite Thematic Score Calculation:**\n"
            report += " - Formula: $$ \\text{Composite Thematic Score} = (\\text{Normalized Keyword Score} \\times 50) + (\\text{Diversity Score} \\times 0.5) $$\n"
            report += f" - Calculation Steps: ({result['normalized_keyword_score']:.4f} × 50) + ({result['diversity_score']:.2f} × 0.5) = {result['normalized_keyword_score']*50:.2f} + {result['diversity_score']*0.5:.2f} = {result['composite_thematic_score']:.2f}\n"
            report += f" - Result: **{result['composite_thematic_score']:.2f}**\n\n"
        
        # Compile the final recommendations
        report += "### Final Recommendation:\n"
        for i, result in enumerate(results, 1):
            report += f"#### Briefing {result['briefing_id']}:\n"
            report += f"- **Composite Thematic Score:** {result['composite_thematic_score']:.2f}\n"
            report += f"- **Normalized Keyword Score:** {result['normalized_keyword_score']:.4f}\n"
            report += f"- **Thematic Intensity:** {result['thematic_intensity']}\n"
            report += f"- **Recommended Action:** {result['recommendation']}\n\n"
        
        report += "### Feedback and Rating:\n"
        report += "Please rate the quality of this summary on a scale of 1 to 5 and provide any remarks for improvement.\n"
        
        return report

def main():
    """Example usage of the InvestorBriefingExtractor class."""
    extractor = InvestorBriefingExtractor()
    
    # Example JSON input
    json_data = '''
    {
  "briefings": [
    {
      "briefing_id": "B311",
      "date": "2023-07-11",
      "briefing_text": "The company shows significant growth driven by innovative solutions.",
      "key_metrics": 96
    },
    {
      "briefing_id": "B312",
      "date": "2023-07-12",
      "briefing_text": "Market trends indicate robust performance with strategic planning.",
      "key_metrics": 94
    },
    {
      "briefing_id": "B313",
      "date": "2023-07-13",
      "briefing_text": "Risk management remains a top priority amid uncertain conditions.",
      "key_metrics": 92
    },
    {
      "briefing_id": "B314",
      "date": "2023-07-14",
      "briefing_text": "Innovation in product development fuels expansion into new markets.",
      "key_metrics": 95
    },
    {
      "briefing_id": "B315",
      "date": "2023-07-15",
      "briefing_text": "Confidence in long-term growth is bolstered by strategic investments.",
      "key_metrics": 93
    },
    {
      "briefing_id": "B316",
      "date": "2023-07-16",
      "briefing_text": "Opportunities for improvement are identified through comprehensive analysis.",
      "key_metrics": 91
    },
    {
      "briefing_id": "B317",
      "date": "2023-07-17",
      "briefing_text": "The briefing highlights challenges and provides a roadmap for risk mitigation.",
      "key_metrics": 90
    },
    {
      "briefing_id": "B318",
      "date": "2023-07-18",
      "briefing_text": "A detailed review of market performance reveals key investment areas.",
      "key_metrics": 92
    },
    {
      "briefing_id": "B319",
      "date": "2023-07-19",
      "briefing_text": "Strategic initiatives and innovative practices drive the company's success.",
      "key_metrics": 94
    },
    {
      "briefing_id": "B320",
      "date": "2023-07-20",
      "briefing_text": "The report outlines opportunities for expansion along with risk assessment.",
      "key_metrics": 93
    }
  ]
}
    '''
    
    print("Processing JSON data...")
    is_valid, records, validation_report, errors = extractor.validate_data(json_data, "json")
    print(validation_report)
    
    if is_valid:
        final_report = extractor.process_briefings(records)
        print(final_report)
    
    # Example CSV input
#     csv_data = '''briefing_id,date,briefing_text,key_metrics
# B013,2023-04-10,"The company exhibits impressive growth and market expansion with innovative approaches.",93
# B014,2023-04-11,"A comprehensive review highlights risk management and strategic investments.",88
# B015,2023-04-12,"The focus is on opportunity identification and overcoming challenges in the current market.",90
# B016,2023-04-13,"Innovation drives the company's vision along with strong confidence in market performance.",87
# B017,2023-04-14,"Strategic initiatives and growth prospects are well-communicated with clear investment guidelines.",92
# B018,2023-04-15,"The briefing provides an insightful perspective on market risks and expansion opportunities.",89
# '''
    
#     print("\nProcessing CSV data...")
#     is_valid, records, validation_report, errors = extractor.validate_data(csv_data, "csv")
#     print(validation_report)
    
    # if is_valid:
    #     final_report = extractor.process_briefings(records)
    #     print(final_report)

if __name__ == "__main__":
    main()