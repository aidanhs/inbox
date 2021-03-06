from tests.util.base import config

# Need to set up test config before we can import from
# inbox.models.tables.
config()
from inbox.models import Participant
from default_event import default_event

# STOPSHIP(emfree): Test multiple distinct remote providers


def test_add_participant(db, config):
    """Test the basic logic of the merge() function."""
    base = default_event(db.session)
    participant = Participant(email_address="foo@example.com")
    remote = default_event(db.session)
    remote.participants = [participant]

    dest = default_event(db.session)

    dest.merge_from(base, remote)
    assert len(dest.participants) == 1


def test_update_participant_status(db, config):
    """Test the basic logic of the merge() function."""
    base = default_event(db.session)
    base.participants = [Participant(email_address="foo@example.com")]

    dest = default_event(db.session)
    dest.participants = [Participant(email_address="foo@example.com")]

    participant1 = Participant(email_address="foo@example.com",
                               status="yes")
    remote = default_event(db.session)
    remote.participants = [participant1]

    dest.merge_from(base, remote)
    assert len(dest.participants) == 1
    assert dest.participants[0].status == 'yes'


def test_update_participant_status2(db, config):
    """Test the basic logic of the merge() function."""
    base = default_event(db.session)
    base.participants = [Participant(email_address="foo@example.com",
                                     status="no")]

    dest = default_event(db.session)
    dest.participants = [Participant(email_address="foo@example.com",
                                     status="no")]

    participant1 = Participant(email_address="foo@example.com",
                               status="yes")
    remote = default_event(db.session)
    remote.participants = [participant1]

    dest.merge_from(base, remote)
    assert len(dest.participants) == 1
    assert dest.participants[0].status == 'yes'


def test_multi_update(db, config):
    """Test the basic logic of the merge() function."""
    base = default_event(db.session)
    base.participants = [Participant(email_address="foo@example.com",
                                     status="no")]

    dest = default_event(db.session)
    dest.participants = [Participant(email_address="foo@example.com",
                                     status="no"),
                         Participant(email_address="foo2@example.com",
                                     status="no")]

    participant1 = Participant(email_address="foo@example.com",
                               status="yes")
    remote = default_event(db.session)
    remote.participants = [participant1]

    dest.merge_from(base, remote)
    assert len(dest.participants) == 2
    for p in dest.participants:
        if p.email_address == "foo@example.com":
            assert p.status == "yes"
        if p.email_address == "foo2@example.com":
            assert p.status == "no"
