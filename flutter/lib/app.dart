import 'package:flutter/material.dart';
import 'www_main.dart';

class WerWieWasApp extends StatelessWidget {
  const WerWieWasApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Who What Where?',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blueGrey.shade50),
        useMaterial3: true,
      ),
      home: const WWWMain(
        title: 'Who What Where?',
        subtitle: 'Speech Driven WWW Query App.',
      ),
    );
  }
}
