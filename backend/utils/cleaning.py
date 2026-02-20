import pandas as pd
from backend.extensions import db
from backend.models.lead import Lead
from sqlalchemy.exc import IntegrityError 
# from flask import current_app # REMOVED: Rely on request context
import sys # Kept for debugging print statements

def clean_and_insert_leads(df: pd.DataFrame, source: str) -> dict:
    inserted_count = 0
    skipped_count = 0
    warnings = []

    # Loop through each row of the Pandas DataFrame. NO CONTEXT WRAPPER HERE.
    for index, row in df.iterrows():
        try:
            # 1. Create the Lead object from the row data
            lead = Lead(
                name=row.get("name"),
                email=row.get("email"),
                company=row.get("company"),
                job_title=row.get("job_title"),
                linkedin_url=row.get("linkedin_url"),
                phone=row.get("phone"),
                location=row.get("location"),
                industry=row.get("industry"),
                source=source
            )
            db.session.add(lead)
            inserted_count += 1
            
        except IntegrityError as e:
            # IntegrityError often happens when data violates a NOT NULL constraint
            db.session.rollback()
            skipped_count += 1
            warnings.append(f"Row {index + 1}: Skipped due to IntegrityError.")
            print(f"DEBUGGING ERROR (IntegrityError) on row {index + 1}: {e}", file=sys.stderr)
        except Exception as e:
            # General exception handler for data type/length errors
            db.session.rollback()
            skipped_count += 1
            warnings.append(f"Row {index + 1}: Skipped due to unknown error.")
            print(f"DEBUGGING ERROR (General Exception) on row {index + 1}: {e}", file=sys.stderr)
    
    # 5. FINAL COMMIT: This uses the session opened by the request context.
    try:
        if inserted_count > 0:
            db.session.commit()
            
    except Exception as e:
        # If the commit fails (e.g., due to final transaction block error)
        db.session.rollback()
        warnings.append(f"Critical Commit Error: Transaction failed to complete: {e}")
        print(f"DEBUGGING ERROR (Final Commit Error): {e}", file=sys.stderr)
        inserted_count = 0 

    return {
        "inserted": inserted_count,
        "skipped": skipped_count,
        "warnings": warnings
    }