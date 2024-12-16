import 'dart:convert';
import 'package:http/http.dart' as http;

Future<String> generateAnswer(String homepage, String query) async {
  try {
    final uri = Uri.parse("http://127.0.0.1:8000/process-rag/");
    final request = http.MultipartRequest('POST', uri)
      ..fields['homepage'] = homepage
      ..fields['query'] = query;

    final response = await request.send();
    final res = await http.Response.fromStream(response);

    if (response.statusCode == 200) {      
      final String responseBody = utf8.decode(res.bodyBytes); // Proper UTF-8 decoding
      final data = json.decode(responseBody);
      return data['answer'] ?? '';
    }
    return "Error: ${response.statusCode}";
  } catch (e) {
    return "RAG failed: $e";
  }
}
