from bindai_core.container import (
    BindContainer,
    ServiceLifetime,
)


class Service:
    pass


def test_register_and_resolve():

    container = BindContainer()

    service = Service()

    container.register(
        Service,
        service,
    )

    assert container.resolve(Service) is service


def test_is_registered():

    container = BindContainer()

    container.register(
        Service,
        Service(),
    )

    assert container.is_registered(Service)


def test_clear():

    container = BindContainer()

    container.register(
        Service,
        Service(),
    )

    container.clear()

    assert not container.is_registered(Service)


def test_resolve_missing_service():

    container = BindContainer()

    try:

        container.resolve(Service)

        assert False

    except KeyError:

        assert True


def test_register_with_lifetime():

    container = BindContainer()

    service = Service()

    container.register(
        Service,
        service,
        ServiceLifetime.SINGLETON,
    )

    assert container.resolve(Service) is service