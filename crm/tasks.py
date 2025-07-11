from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .cron import log_crm_heartbeat, update_low_stock, generate_crm_report_task

@shared_task
def log_crm_heartbeat_task():
    """Celery task wrapper for CRM heartbeat logging"""
    try:
        log_crm_heartbeat()
        return "Heartbeat logged successfully"
    except Exception as e:
        return f"Heartbeat logging failed: {str(e)}"

@shared_task
def update_low_stock_task():
    """Celery task wrapper for low stock updates"""
    try:
        update_low_stock()
        return "Low stock update completed successfully"
    except Exception as e:
        return f"Low stock update failed: {str(e)}"

@shared_task
def generate_crm_report():
    """Celery task wrapper for CRM report generation"""
    try:
        generate_crm_report_task()
        return "CRM report generated successfully"
    except Exception as e:
        return f"CRM report generation failed: {str(e)}"

@shared_task
def debug_task():
    """Simple debug task for testing Celery"""
    return "Debug task executed successfully"
