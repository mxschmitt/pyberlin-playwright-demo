from typing import Generator

import pytest

from playwright.sync_api import Page, expect

from .utils import TODO_ITEMS, create_default_todos


@pytest.fixture(autouse=True)
def run_around_tests(page: Page) -> Generator[None, None, None]:
    # setup before a test
    page.goto("https://demo.playwright.dev/todomvc")
    create_default_todos(page)
    # run the actual test
    yield
    # run any cleanup code


def test_should_display_the_correct_text(page: Page) -> None:
    page.locator(".todo-list li .toggle").first.check()
    expect(page.locator(".clear-completed")).to_have_text("Clear completed")


def test_should_clear_completed_items_when_clicked(page: Page) -> None:
    todo_items = page.locator(".todo-list li")
    todo_items.nth(1).locator(".toggle").check()
    page.locator(".clear-completed").click()
    expect(todo_items).to_have_count(2)
    expect(todo_items).to_have_text([TODO_ITEMS[0], TODO_ITEMS[2]])


def test_should_be_hidden_when_there_are_no_items_that_are_completed(
    page: Page,
) -> None:
    page.locator(".todo-list li .toggle").first.check()
    page.locator(".clear-completed").click()
    expect(page.locator(".clear-completed")).to_be_hidden()
