import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, String>> generateAnswer(
    String homepage, String query) async {
  try {
    final uri = Uri.parse("http://127.0.0.1:8000/process-rag/");
    final request = http.MultipartRequest('POST', uri)
      ..fields['homepage'] = homepage
      ..fields['query'] = query;

    final response = await request.send();
    final res = await http.Response.fromStream(response);

    if (response.statusCode == 200) {
      final String responseBody =
          utf8.decode(res.bodyBytes); // Proper UTF-8 decoding
      final data = json.decode(responseBody);

      final String ragAnswer = data['answer'] ?? '';
      final bool failed = ragAnswer == "" || ragAnswer == "Not Found.";
      return {
        "answer": ragAnswer,
        "status": failed ? "failed" : "successful",
      };
    }
    return {
      "answer": "Error: ${response.statusCode}",
      "status": "failed",
    };
  } catch (e) {
    return {
      "answer": "RAG failed: $e",
      "status": "failed",
    };
  }
}
