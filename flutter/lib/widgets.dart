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

Widget _buildProcessingIndicator(bool status) {
  return status
      ? SizedBox(
          width: 24,
          height: 24,
          child: CircularProgressIndicator(
            strokeWidth: 2.0,
          ),
        )
      : Icon(
          Icons.check_circle,
          color: Colors.green,
        );
}

Widget buildStatus(
    BuildContext context, bool processing1, bool processing2, bool processing3) {
  if (processing1 == false && processing2 == false && processing3 == false) {
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
