"""Optimizer module."""

from sympy import Symbol, simplify_logic, Not
from .InverseIndex import idx

import logging


def get_ocurrences(symbol):
    """Get the ocurrences of a symbol."""
    if isinstance(symbol, Not):
        symbol = symbol.args[0]

    return idx.ocurrences[str(symbol)]


def key_terms(terms):
    """Get the key terms (first) of a list of terms."""
    match terms:
        case list():
            return get_ocurrences(terms[0])
        case _:
            return get_ocurrences(terms)


def sort_inners(terms):
    """Sort the terms in the query."""
    logging.debug("Sorting terms: %s", terms)

    sorted_terms = []

    for term in terms:
        if isinstance(term, Symbol) or isinstance(term, Not):
            sorted_terms.append(term)
            continue
        logging.debug("Sorting term: %s", term)

        symbols = sorted(term.args, key=get_ocurrences)

        logging.debug("Sorted term: %s", symbols)

        sorted_terms.append(symbols)

    return sorted(sorted_terms, key=key_terms)


def generate_query(sorted_terms):
    """Generate a query from a list of sorted terms."""
    response = set()

    all_files = set(file for files in idx.values() for file in files)

    print("all file", all_files)

    print("sorted terms", sorted_terms)

    for term in sorted_terms:

        if isinstance(term, Not):
            term = term.args[0]
            response.update(all_files.difference(idx[str(term)]))
            continue

        if isinstance(term, Symbol):
            response.update(idx[str(term)])
            continue

        and_response = all_files.copy()  # Start with all files
        for symbol in term:
            if isinstance(term, Not):
                and_response.difference_update(idx[str(term.args[0])])
            else:
                and_response.intersection_update(idx[str(symbol)])

        response.update(and_response)

    return response


def Optimize(query):
    """Optimize the query."""

    for keyword in query.free_symbols:
        logging.info(f"{keyword}:  {idx[str(keyword)]}")

    if isinstance(query, Symbol):
        return idx[str(query)]

    logging.debug("Optimizing query: %s", query)

    symplified_query = simplify_logic(query)

    logging.info("Symplyfied query: %s", symplified_query)

    terms = symplified_query.args

    sorted = sort_inners(terms)

    return generate_query(sorted)
