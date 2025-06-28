from crawler import extract_page_content
from analyzer import analyze_seo_with_gpt35

if __name__ == "__main__":
    url = input("🔗 Enter a URL to analyze: ").strip()
    page_data = extract_page_content(url)

    if page_data:
        print("\n📊 GPT-3.5 SEO Insights:\n")
        report = analyze_seo_with_gpt35(page_data)
        print(report)
    else:
        print("❌ Could not extract page content.")
