# Day 22 - SOLVED: OrderStatus (Enum) and describe_order (using Literal) are
# worked together in the session. PaymentInfo (TypedDict) and Money
# (dataclass) are today's "Your turn" items 1-2 - marked with # TODO.

from dataclasses import dataclass
from enum import Enum
from typing import Literal, TypedDict


class OrderStatus(str, Enum):
    PENDING = "pending"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


def describe_order(status: OrderStatus, style: Literal["short", "long"] = "short") -> str:
    if style == "short":
        return status.value
    messages = {
        OrderStatus.PENDING: "Your order is being prepared.",
        OrderStatus.SHIPPED: "Your order is on its way.",
        OrderStatus.DELIVERED: "Your order has arrived!",
        OrderStatus.CANCELLED: "Your order was cancelled.",
    }
    return messages[status]


# TODO 1: PaymentInfo - a TypedDict with amount: float, currency: str,
# status: str. No validation needed, this just documents an external shape.
# class PaymentInfo(TypedDict):
#     ...


# TODO 2: Money - a @dataclass with amount: float and currency: str, plus a
# formatted() method returning e.g. "1,500 XAF" for Money(1500, "XAF").
# @dataclass
# class Money:
#     ...
#     def formatted(self) -> str:
#         ...
