import 'dart:convert';
import 'package:universal_io/io.dart';
import 'package:audio_waveforms/audio_waveforms.dart';
import 'package:http/http.dart' as http;

Future<Map<String, String>> stopAndUpload(
    RecorderController recorderController, String queryPage) async {
  final path = await recorderController.stop();
  if (path == null) {
    return {
      "answer": "Recorder didn't return a valid file.",
      "status": "failed",
    };
  }

  try {
    final file = File(path);
    final uri = Uri.parse("http://127.0.0.1:8000/process-audio/");
    final request = http.MultipartRequest('POST', uri)
      ..fields['url'] = queryPage
      ..files.add(await http.MultipartFile.fromPath('file', file.path));

    final response = await request.send();
    final res = await http.Response.fromStream(response);

    if (response.statusCode == 200) {
      final String responseBody =
          utf8.decode(res.bodyBytes); // Proper UTF-8 decoding
      final data = json.decode(responseBody);
      final String question = data['question'] ?? '';
      return {
        "question": question,
        "status": question != "" ? "successful" : "failed",
      };
    }
    return {
      "question": "Error: ${response.statusCode}",
      "status": "failed",
    };
  } catch (e) {
    return {
      "question": "RAG failed: $e",
      "status": "failed",
    };
  }
}
