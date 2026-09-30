from core.flows.complex_search.flow import build_complex_flow


def main():

    flow = build_complex_flow()

    with flow:
        flow.block()


if __name__ == '__main__':
    main()
