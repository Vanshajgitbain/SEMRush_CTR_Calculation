import streamlit as st
import pandas as pd
import openpyxl
from openpyxl.styles import Font
from io import BytesIO
import io

st.set_page_config(page_title="CTR Processor", layout="wide")

def identify_company(keywords_list):
    """
    Identify company from keywords in the file.
    Returns the identified company name.
    """
    keywords_lower = [str(kw).lower() for kw in keywords_list if pd.notna(kw)]
    
    company_indicators = {
        'Bank of America': ['bank of america', 'bofa', 'b of a'],
        'Wells Fargo': ['wells fargo', 'wellsfargo'],
        'Citibank': ['citibank', 'citi'],
        'Chase': ['chase', 'jp morgan chase', 'jpmorgan'],
        'Capital One': ['capital one'],
        'American Express': ['american express', 'amex'],
    }
    
    company_counts = {company: 0 for company in company_indicators}
    
    for keyword in keywords_lower:
        for company, indicators in company_indicators.items():
            for indicator in indicators:
                if indicator in keyword:
                    company_counts[company] += 1
    
    if max(company_counts.values()) > 0:
        return max(company_counts, key=company_counts.get)
    else:
        return 'Unknown Company'

def process_excel_files(uploaded_files):
    """
    Process all uploaded Excel files.
    Returns aggregated data by company.
    """
    if not uploaded_files:
        return None
    
    monthly_data = []
    company_aggregates = {}
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    for idx, uploaded_file in enumerate(uploaded_files):
        status_text.text(f"Processing: {uploaded_file.name}")
        
        try:
            df = pd.read_excel(uploaded_file, sheet_name=0)
            
            # Extract columns D (index 3) and H (index 7)
            search_volume_col = df.iloc[:, 3]  # Column D
            traffic_col = df.iloc[:, 7]  # Column H
            
            # Get keywords from first column to identify company
            keywords = df.iloc[:, 0]
            
            # Identify company
            company = identify_company(keywords.tolist())
            
            # Calculate monthly totals
            monthly_search_volume = pd.to_numeric(search_volume_col, errors='coerce').sum()
            monthly_traffic = pd.to_numeric(traffic_col, errors='coerce').sum()
            
            # Store monthly data
            monthly_data.append({
                'File Name': uploaded_file.name,
                'Company': company,
                'Monthly Search Volume': int(monthly_search_volume) if pd.notna(monthly_search_volume) else 0,
                'Monthly Traffic': int(monthly_traffic) if pd.notna(monthly_traffic) else 0
            })
            
            # Aggregate by company for yearly calculations
            if company not in company_aggregates:
                company_aggregates[company] = {
                    'Total Search Volume': 0,
                    'Total Traffic': 0
                }
            
            company_aggregates[company]['Total Search Volume'] += monthly_search_volume
            company_aggregates[company]['Total Traffic'] += monthly_traffic
            
        except Exception as e:
            st.error(f"Error processing {uploaded_file.name}: {str(e)}")
            continue
        
        progress_bar.progress((idx + 1) / len(uploaded_files))
    
    status_text.empty()
    progress_bar.empty()
    
    # Calculate CTR and prepare company summary
    company_summary = []
    for company, data in sorted(company_aggregates.items()):
        total_search_volume = data['Total Search Volume']
        total_traffic = data['Total Traffic']
        ctr = total_traffic / total_search_volume if total_search_volume > 0 else 0
        
        company_summary.append({
            'Company': company,
            'Total Search Volume': int(total_search_volume),
            'Total Traffic': int(total_traffic),
            'CTR': ctr
        })
    
    return {
        'company_summary': company_summary,
        'monthly_data': monthly_data
    }

def generate_output_excel(results):
    """
    Generate the output Excel file with two sheets.
    Returns BytesIO object.
    """
    if not results:
        return None
    
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    
    # Sheet 1: Company Summary
    ws1 = wb.create_sheet('Company Summary', 0)
    ws1.append(['Company', 'Total Search Volume', 'Total Traffic', 'CTR'])
    
    for row in results['company_summary']:
        ws1.append([
            row['Company'],
            row['Total Search Volume'],
            row['Total Traffic'],
            row['CTR']
        ])
    
    # Sheet 2: Monthly Summary
    ws2 = wb.create_sheet('Monthly Summary', 1)
    ws2.append(['File Name', 'Company', 'Monthly Search Volume', 'Monthly Traffic'])
    
    for row in results['monthly_data']:
        ws2.append([
            row['File Name'],
            row['Company'],
            row['Monthly Search Volume'],
            row['Monthly Traffic']
        ])
    
    # Save to BytesIO
    output = BytesIO()
    wb.save(output)
    output.seek(0)
    return output

# Streamlit UI
st.title("📊 CTR Processor")
st.markdown("Upload multiple Excel files to calculate yearly CTR by company")

st.divider()

# File upload section
st.subheader("Step 1: Upload Excel Files")
uploaded_files = st.file_uploader(
    "Choose Excel files (.xlsx, .xls)",
    type=['xlsx', 'xls'],
    accept_multiple_files=True
)

if uploaded_files:
    st.success(f"✅ {len(uploaded_files)} file(s) uploaded")
    
    # Process button
    if st.button("🔄 Process Files", type="primary", use_container_width=True):
        st.divider()
        results = process_excel_files(uploaded_files)
        
        if results:
            st.session_state['results'] = results
            st.success("✅ Files processed successfully!")
            
            # Display results
            st.subheader("Company Summary")
            summary_df = pd.DataFrame(results['company_summary'])
            st.dataframe(summary_df, use_container_width=True, hide_index=True)
            
            st.subheader("Monthly Summary")
            monthly_df = pd.DataFrame(results['monthly_data'])
            st.dataframe(monthly_df, use_container_width=True, hide_index=True)
            
            st.divider()
            
            # Download button
            excel_file = generate_output_excel(results)
            st.download_button(
                label="📥 Download CTR_Summary.xlsx",
                data=excel_file,
                file_name="CTR_Summary.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
else:
    st.info("👆 Upload Excel files to get started")

st.divider()

# Footer with information
st.markdown("""
---
**How it works:**
- Upload 1 or more Excel files (monthly data)
- Files are processed to extract Column D (Search Volume) and Column H (Traffic)
- Company is identified from keywords
- CTR is calculated as: Traffic ÷ Search Volume
- Download the summary Excel file with results
""")
