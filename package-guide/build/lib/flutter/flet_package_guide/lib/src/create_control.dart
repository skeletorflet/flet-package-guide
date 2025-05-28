import 'package:flet/flet.dart';

import 'flet_package_guide.dart';

CreateControlFactory createControl = (CreateControlArgs args) {
  switch (args.control.type) {
    case "flet_package_guide":
      return FletPackageGuideControl(
        parent: args.parent,
        control: args.control,
        children: args.children,
        parentDisabled: args.parentDisabled,
        parentAdaptive: args.parentAdaptive,
        backend: args.backend,
      );
    default:
      return null;
  }
};

void ensureInitialized() {
  // nothing to initialize
}
