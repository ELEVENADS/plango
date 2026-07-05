import logging
import socket

import nacos

from app.core.config import settings

logger = logging.getLogger(__name__)

_client: nacos.NacosClient | None = None


def _get_client() -> nacos.NacosClient:
    global _client
    if _client is None:
        _client = nacos.NacosClient(settings.nacos_server_addr)
    return _client


def _resolve_ip() -> str:
    if settings.nacos_service_ip:
        return settings.nacos_service_ip
    try:
        return socket.gethostbyname(socket.gethostname())
    except Exception:
        return settings.host


def register_service() -> None:
    client = _get_client()
    ip = _resolve_ip()
    try:
        client.add_naming_instance(
            settings.nacos_service_name,
            ip,
            settings.nacos_service_port,
            group_name=settings.nacos_group,
        )
        logger.info(
            "Registered %s at Nacos (%s:%s, group=%s)",
            settings.nacos_service_name,
            ip,
            settings.nacos_service_port,
            settings.nacos_group,
        )
    except Exception:
        logger.exception("Failed to register with Nacos")


def deregister_service() -> None:
    client = _get_client()
    ip = _resolve_ip()
    try:
        client.remove_naming_instance(
            settings.nacos_service_name,
            ip,
            settings.nacos_service_port,
            group_name=settings.nacos_group,
        )
        logger.info("Deregistered %s from Nacos", settings.nacos_service_name)
    except Exception:
        logger.exception("Failed to deregister from Nacos")
