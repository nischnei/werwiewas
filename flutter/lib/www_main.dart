import 'package:flutter/material.dart';
import 'package:audio_waveforms/audio_waveforms.dart';
import 'package:permission_handler/permission_handler.dart';
import 'page_service.dart';
import 'rag_service.dart';
import 'recorder_service.dart';
import 'widgets.dart';

class WWWMain extends StatefulWidget {
  const WWWMain({super.key, required this.title, required this.subtitle});

  final String title;
  final String subtitle;

  @override
  State<WWWMain> createState() => _WWWMainState();
}

class _WWWMainState extends State<WWWMain> {
  String _queryPage = "";
  bool _isRecording = false;
  String _processingSpeech = "init";
  String _processingPage = "init";
  String _processingAnswer = "init";
  String _backendPageContent = "";
  String _backendQuestion = "";
  String _backendAnswer = "";
  final RecorderController _recorderController = RecorderController();

  @override
  void initState() {
    super.initState();
    _requestMicrophonePermission();
  }

  Future<void> _requestMicrophonePermission() async {
    await Permission.microphone.request();
  }

  @override
  void dispose() {
    _recorderController.dispose();
    super.dispose();
  }

  void _toggleRecording() async {
    if (_isRecording) {
      setState(() {
        _isRecording = false;
        _processingSpeech = "processing";
        _processingPage = "processing";
        _processingAnswer = "processing";
      });

      Future<Map<String, String>> page = parsePage(_queryPage);
      Future<Map<String, String>> question = stopAndUpload(_recorderController, _queryPage);

      page.then((result) {
        setState(() {
          _backendPageContent = result["homepage"] ?? "";
          _processingPage = result["status"] ?? "failed";
        });
      });

      question.then((result) {
        setState(() {
          _backendQuestion = result["question"] ?? "";
          _processingSpeech = result["status"] ?? "failed";
        });
      });

      await Future.wait([page, question]);
      final answer =
          await generateAnswer(_backendPageContent, _backendQuestion);
      setState(() {
        _processingAnswer = answer["status"] ?? "failed";
        _backendAnswer = answer["answer"] ?? "";
      });
    } else {
      await _recorderController.record();
      setState(() {
        _isRecording = true;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: buildAppBar(widget.title, widget.subtitle, context),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            const SizedBox(height: 10),
            const Text('Homepage to query:'),
            const SizedBox(height: 10),
            SizedBox(
              width: 250,
              child: TextField(
                onChanged: (text) => setState(() => _queryPage = text),
                obscureText: false,
                decoration: const InputDecoration(
                  border: OutlineInputBorder(),
                  labelText: 'https://',
                ),
              ),
            ),
            Text(_queryPage),
            const SizedBox(height: 30),
            _isRecording
                ? buildAudioWaveform(context, _recorderController)
                : buildStatus(context, _processingSpeech, _processingPage, _processingAnswer),
            const SizedBox(height: 30),
            FloatingActionButton(
              onPressed: _toggleRecording,
              tooltip: _isRecording ? 'Stop Recording' : 'Start Speech Query',
              backgroundColor: _isRecording
                  ? Colors.red
                  : Theme.of(context).colorScheme.inversePrimary,
              child: const Icon(Icons.mic),
            ),
            const SizedBox(height: 30),
            const Text("Question:"),
            Text(_backendQuestion),
            const SizedBox(height: 10),
            const Text("Answer:"),
            Text(_backendAnswer),
            const Spacer(),
          ],
        ),
      ),
    );
  }
}
