import 'dart:convert';
import 'package:http/http.dart' as http;

Future<Map<String, String>> parsePage(String url) async {
  try {
    final uri = Uri.parse("http://127.0.0.1:8000/process-url/");
    final request = http.MultipartRequest('POST', uri)
      ..fields['url'] = url;

    final response = await request.send();
    final res = await http.Response.fromStream(response);

    if (response.statusCode == 200) {
      final String responseBody = utf8.decode(res.bodyBytes); // Proper UTF-8 decoding
      final data = json.decode(responseBody);
      final String homepageContent = data['homepage'] ?? '';
      return {
        "homepage": homepageContent,
        "status": homepageContent != "" ? "successful" : "failed",
      };
    }
    return {
      "homepage": "Error: ${response.statusCode}",
      "status": "failed",
    };
  } catch (e) {
    return {
      "homepage": "Homepage parsing failed: $e",
      "status": "failed",
    };
  }
}
