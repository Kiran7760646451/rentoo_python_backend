from fastapi import FastAPI, HTTPException
from .models import OwnerCreate, Owner, PropertyCreate, Property
from .database import get_db_connection
import pymysql
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Rentoo API", description="Property Management API")


@app.post("/owners/", response_model=Owner)
async def create_owner(owner: OwnerCreate):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = """
                INSERT INTO owner (name, email, phone)
                VALUES (%s, %s, %s)
            """
            try:
                cursor.execute(sql, (owner.name, owner.email, owner.phone))
                connection.commit()

                # Get the created owner
                owner_id = cursor.lastrowid
                cursor.execute(
                    "SELECT * FROM owner WHERE id = %s", (owner_id,))
                result = cursor.fetchone()

                if not result:
                    raise HTTPException(
                        status_code=404, detail="Owner not found after creation")

                return Owner(**result)
            except pymysql.Error as e:
                logger.error(f"Database error: {str(e)}")
                raise HTTPException(
                    status_code=400, detail=f"Database error: {str(e)}")
    except Exception as e:
        logger.error(f"Error creating owner: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        connection.close()


@app.post("/properties/", response_model=Property)
async def create_property(property: PropertyCreate):
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # First check if owner exists
            cursor.execute("SELECT id FROM owner WHERE id = %s",
                           (property.owner_id,))
            if not cursor.fetchone():
                raise HTTPException(status_code=404, detail="Owner not found")

            # Check property limit
            cursor.execute(
                "SELECT COUNT(*) as count FROM property WHERE owner_id = %s",
                (property.owner_id,)
            )
            result = cursor.fetchone()
            if result['count'] >= 5:
                raise HTTPException(
                    status_code=400,
                    detail="Owner has reached the maximum limit of 5 properties"
                )

            # Check if property name already exists for this owner
            cursor.execute(
                "SELECT id FROM property WHERE owner_id = %s AND property_name = %s",
                (property.owner_id, property.property_name)
            )
            if cursor.fetchone():
                raise HTTPException(
                    status_code=400,
                    detail="A property with this name already exists for this owner"
                )

            # Insert new property
            sql = """
                INSERT INTO property (
                    owner_id, property_name, address, city, state, zip_code, 
                    monthly_rent, status
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            try:
                cursor.execute(sql, (
                    property.owner_id,
                    property.property_name,
                    property.address,
                    property.city,
                    property.state,
                    property.zip_code,
                    property.monthly_rent,
                    property.status
                ))
                connection.commit()

                # Get the created property
                property_id = cursor.lastrowid
                cursor.execute(
                    "SELECT * FROM property WHERE id = %s", (property_id,))
                result = cursor.fetchone()

                if not result:
                    raise HTTPException(
                        status_code=404, detail="Property not found after creation")

                return Property(**result)
            except pymysql.Error as e:
                logger.error(f"Database error: {str(e)}")
                if "unique_owner_property_name" in str(e):
                    raise HTTPException(
                        status_code=400,
                        detail="A property with this name already exists for this owner"
                    )
                raise HTTPException(
                    status_code=400, detail=f"Database error: {str(e)}")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error creating property: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Internal server error: {str(e)}")
    finally:
        connection.close()


@app.get("/")
async def root():
    return {"message": "Welcome to Rentoo API"}
