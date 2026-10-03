# ============================================================
# EcoAgent - Database
# ============================================================

import sqlite3


DATABASE_NAME = "ecoagent.db"


# ============================================================
# CREATE DATABASE AND TABLE
# ============================================================

def initialize_database():
    """
    Create the EcoAgent database and analysis history table.
    """

    connection = sqlite3.connect(DATABASE_NAME)

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            device_type TEXT,
            brand TEXT,
            model TEXT,

            age INTEGER,

            physical_condition TEXT,
            power_status TEXT,
            battery_condition TEXT,

            main_problem TEXT,

            recommendation TEXT,
            reason TEXT,

            device_weight REAL,
            useful_life TEXT,

            analysis_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    connection.close()


# ============================================================
# SAVE ANALYSIS
# ============================================================

def save_analysis(
    device_data,
    decision,
    impact
):
    """
    Save one EcoAgent analysis into the database.
    """

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO analysis_history (
            device_type,
            brand,
            model,
            age,
            physical_condition,
            power_status,
            battery_condition,
            main_problem,
            recommendation,
            reason,
            device_weight,
            useful_life
        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (

        device_data.get("device_type"),
        device_data.get("brand"),
        device_data.get("model"),

        device_data.get("age"),

        device_data.get("physical_condition"),
        device_data.get("power_status"),
        device_data.get("battery_condition"),

        device_data.get("main_problem"),

        decision.get("recommendation"),
        decision.get("reason"),

        impact.get("device_weight"),
        impact.get("useful_life")
    ))

    connection.commit()
    connection.close()


# ============================================================
# GET ANALYSIS HISTORY
# ============================================================

def get_analysis_history():
    """
    Return all previous EcoAgent analyses.
    """

    connection = sqlite3.connect(
        DATABASE_NAME
    )

    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            id,
            device_type,
            brand,
            model,
            age,
            recommendation,
            device_weight,
            useful_life,
            analysis_date

        FROM analysis_history

        ORDER BY id DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records