import AppKit
import AVFoundation
import Foundation

let file = URL(fileURLWithPath: CommandLine.arguments[1])
let directory = URL(fileURLWithPath: CommandLine.arguments[2], isDirectory: true)
let asset = AVURLAsset(url: file)
print("duration=\(CMTimeGetSeconds(asset.duration)) videoTracks=\(asset.tracks(withMediaType: .video).count) audioTracks=\(asset.tracks(withMediaType: .audio).count)")
let generator = AVAssetImageGenerator(asset: asset)
generator.appliesPreferredTrackTransform = true
for second in [1, 15, 25] {
    let image = try generator.copyCGImage(at: CMTime(seconds: Double(second), preferredTimescale: 600), actualTime: nil)
    let data = NSBitmapImageRep(cgImage: image).representation(using: .png, properties: [:])!
    try data.write(to: directory.appendingPathComponent("verify-\(second).png"))
}
