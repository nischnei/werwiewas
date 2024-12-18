import 'package:flutter/material.dart';
import 'package:audio_waveforms/audio_waveforms.dart';

PreferredSizeWidget buildAppBar(
    String title, String subtitle, BuildContext context) {
  return AppBar(
    backgroundColor: Theme.of(context).colorScheme.inversePrimary,
    title: Text(title),
    bottom: PreferredSize(
      preferredSize: Size.zero,
      child: Text(subtitle),
    ),
  );
}

Widget buildAudioWaveform(BuildContext context, RecorderController controller) {
  return Center(
    child: AudioWaveforms(
      enableGesture: false,
      size: Size(MediaQuery.of(context).size.width * 0.8, 24),
      recorderController: controller,
      waveStyle: WaveStyle(
        waveColor: Theme.of(context).colorScheme.inversePrimary,
        extendWaveform: true,
        showMiddleLine: false,
        waveThickness: 1.5,
        spacing: 5.0,
        scaleFactor: 200,
      ),
    ),
  );
}

Widget _buildProcessingIndicator(String status) {
  if (status == "failed") {
    return Icon(
      Icons.error,
      color: Colors.red,
    );
  } else if (status == "successful") {
    return Icon(
      Icons.check_circle,
      color: Colors.green,
    );
  } else if (status == "processing") {
    return SizedBox(
      width: 24,
      height: 24,
      child: CircularProgressIndicator(
        strokeWidth: 2.0,
      ),
    );
  } else {
    return Icon(
      Icons.question_mark,
      color: Colors.blue,
    );
  }
}

Widget buildStatus(BuildContext context, String processing1, String processing2,
    String processing3) {
  if (processing1 == "init" && processing2 == "init" && processing3 == "init") {
    return SizedBox(
      height: 24,
    );
  }

  return Row(
    mainAxisAlignment: MainAxisAlignment.spaceAround,
    children: [
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Question:'),
        ],
      ),
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildProcessingIndicator(processing1),
        ],
      ),
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Page:'),
        ],
      ),
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildProcessingIndicator(processing2),
        ],
      ),
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text('Answer:'),
        ],
      ),
      Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          _buildProcessingIndicator(processing3),
        ],
      ),
    ],
  );
}
