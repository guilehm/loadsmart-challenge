import click

from src.models import TrucksAndCargos


@click.command()
@click.option('--verbose/--no-verbose', default=True)
@click.option('--all-combinations/--not-all-combinations', default=False)
def run(verbose, all_combinations):
    trucks_and_cargos = TrucksAndCargos()
    getattr(trucks_and_cargos, 'best_combo')
    if not all_combinations:
        trucks_and_cargos.print_best_combo(verbose=verbose)
    else:
        trucks_and_cargos.print_all_combos(verbose=verbose)


if __name__ == '__main__':
    run()
