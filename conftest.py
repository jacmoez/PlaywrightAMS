# # conftest.py
# import pytest

# @pytest.fixture(scope="session")
# def browser_context_args(browser_context_args):
#     return {
#         **browser_context_args,
#         # Crucial: This stops Playwright from overriding the window with its default 1280x720 box
#         "no_viewport": True, 
#     }