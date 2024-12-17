// This is a basic Flutter widget test. More or less to test if all fires up correctly.

import 'package:flutter_test/flutter_test.dart';
import 'package:www/app.dart';

void main() {
  testWidgets('App initial states as expected smoke test.',
      (WidgetTester tester) async {
    // Build the app and do nothing for now.
    await tester.pumpWidget(const WhoWhatWhereApp());

    // Verify that all is setup
    expect(find.text('Question:'), findsOneWidget);
    expect(find.text('Answer:'), findsOneWidget);
    expect(find.text('Homepage to query:'), findsOneWidget);
  });
}
