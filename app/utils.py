def format_travel_response(raw_response: str) -> str:
    """
        Takes raw response from the Model
        Body:
            raw response:string
        Returns:
            formatted response by adding mardown(double arsterics) which will denote as bold
            joins the lines innew line
    """
    lines = raw_response.split("\n\n")
    structured_response = []
    for line in lines:
        line = line.strip()
        if line.lower().startswith("visa") or "visa" in line.lower():
            structured_response.append(f"**Visa**: {line}")
        elif line.lower().startswith("passport") or "passport" in line.lower():
            structured_response.append(f"**Passport**: {line}")
        elif line.lower().startswith("advis") or "advisory" in line.lower():
            structured_response.append(f"**Travel Advisories**: {line}")
        else:
            structured_response.append(line)
    return "\n".join(structured_response) if structured_response else raw_response
