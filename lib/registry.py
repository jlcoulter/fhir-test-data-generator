from lib.au.registry import BUILDERS as AU_BUILDERS
from lib.hc.registry import BUILDERS as HC_BUILDERS


BUILDERS = {**HC_BUILDERS, **AU_BUILDERS}


def create_generator(args):
    builder_class = BUILDERS.get((args.ig.lower(), args.type.lower()))
    if builder_class is None:
        raise KeyError(f"{args.ig}:{args.type}")
    return builder_class(args)


def available_generator_keys():
    return sorted(f"{profile}:{resource}" for profile, resource in BUILDERS)


def builders_for_ig(ig):
    normalized_ig = ig.lower()
    return {
        resource: builder_class
        for (builder_profile, resource), builder_class in BUILDERS.items()
        if builder_profile == normalized_ig
    }
