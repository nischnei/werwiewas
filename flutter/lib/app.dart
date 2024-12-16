import 'package:flutter/material.dart';
import 'www_main.dart';

class WerWieWasApp extends StatelessWidget {
  const WerWieWasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Wer Wie Was?',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey.shade50),
        useMaterial3: true,
      ),
      home: const WWWMain(
        title: 'Wer Wie Was?',
        subtitle: 'Speech Driven WWW Query App.',
      ),
    );
  }
}
