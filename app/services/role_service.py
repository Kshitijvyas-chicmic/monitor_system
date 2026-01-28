from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.role_db import Role
from app.schemas.role_schema import RoleResponse
from app.core.config_logging import logger


def get_roles(db: Session):
    roles = db.query(Role).all()
    logger.info("Fetched all roles", extra={"count": len(roles)})
    return roles

def get_role_by_name(db: Session, name: str) -> Role:
    logger.info("Fetch role by name request", extra={"role_name": name})
    role = db.query(Role).filter(Role.name == name).first()
    if not role:
        logger.warning("Role not found by name", extra={"role_name": name})
        raise HTTPException(status_code=404, detail=f"Role '{name}' not found")
    logger.info("Role retrieved successfully", extra={"role_id": role.id, "role_name": role.name})
    return role

def get_role_by_id(db: Session, role_id: int) -> Role:
    logger.info("Fetch role by id request", extra={"role_id": role_id})
    role = db.query(Role).filter(Role.id == role_id).first()
    if not role:
        logger.warning("Role not found by id", extra={"role_id": role_id})
        raise HTTPException(status_code=404, detail="Role not found")
    logger.info("Role retrieved successfully", extra={"role_id": role.id, "role_name": role.name})
    return role
