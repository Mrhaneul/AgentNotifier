from agentnotifier.core.output import OutputRingBuffer


def test_output_ring_buffer_tail() -> None:
    ring = OutputRingBuffer(max_lines=3)
    for line in ["line-1", "line-2", "line-3", "line-4"]:
        ring.add_line(line)

    assert ring.tail() == ["line-2", "line-3", "line-4"]
