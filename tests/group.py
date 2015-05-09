# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from sqlautocode_gen.group_model import TrGroup, TrGroupMeeting, TrGroupComment
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class GroupBaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u1.id, title="g2")
        g_list = [cls.g1, cls.g2]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g1.users.append(cls.u3)
        cls.g1.users.append(cls.u4)
        session.add(cls.g1)
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


    def test_relations_user_group(self):

        self.session.add(self.u1)
        self.session.add(self.u3)
        self.session.add(self.u4)
        self.session.add(self.g1)

        self.assertEquals(len(self.g1.users), 2)
        self.assertIn(self.u3, self.g1.users)
        self.assertIn(self.u4, self.g1.users)

    def test_check_properties(self):

        self.session.add(self.u1)
        self.session.add(self.g1)

        self.assertEquals(self.g1.title, "g1")
        self.assertEquals(self.g1.user_id, self.u1.id)


class GroupGetTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)  # one own group
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)  # two own groups
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)  # in one group
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)  # in two groups
        cls.u5 = TrUser(login="55555", type="phone", auth_code="5555", authenticated=True)  # no any groups
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4, cls.u5]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.refresh(cls.u5)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2")
        cls.g3 = TrGroup(user_id=cls.u2.id, title="g3")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g1.users.append(cls.u3)
        cls.g1.users.append(cls.u4)
        cls.g2.users.append(cls.u4)
        session.add_all([cls.g1, cls.g2])
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


    def test_no_groups(self):

        self.session.add(self.u5)

        data = server.getGroups(self.u5.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 0)

    def test_in_one_group_no_own_groups(self):

        self.session.add(self.u3)

        data = server.getGroups(self.u3.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], "g1")
        self.assertEquals(data['result'][0]['admin'], False)
        self.assertEquals(data['result'][0]['invitation'], False)
        self.assertEquals(data['result'][0]['help'], False)

    def test_in_many_groups_one_own_group(self):

        self.session.add(self.u4)

        data = server.getGroups(self.u4.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 2)
        self.assertEquals(data['result'][0]['title'], "g1")
        self.assertEquals(data['result'][0]['admin'], False)
        self.assertEquals(data['result'][1]['title'], "g2")
        self.assertEquals(data['result'][1]['admin'], False)

    def test_in_zero_groups_one_own_group(self):

        self.session.add(self.u1)

        data = server.getGroups(self.u1.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], "g1")
        self.assertEquals(data['result'][0]['admin'], True)

    def test_in_zero_groups_many_own_group(self):

        self.session.add(self.u2)

        data = server.getGroups(self.u2.id)

        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 2)
        self.assertEquals(data['result'][0]['title'], "g2")
        self.assertEquals(data['result'][0]['admin'], True)
        self.assertEquals(data['result'][1]['title'], "g3")
        self.assertEquals(data['result'][1]['admin'], True)


class GroupAddTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)
        u_list = [cls.u1, cls.u2]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2")
        g_list = [cls.g1, cls.g2]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g2.users.append(cls.u1)
        session.add_all([cls.g2])
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()

    # def test_add_group(self):
    #
    #     self.session.add(self.u1)
    #       #TODO: group added in another session. Error in attempt to delete all users and groups
    #     data = server.addGroup(self.u1.id, "group", "desc", True, False, False)
    #
    #     self.assertJsonRpc(data)
    #
    #     s = Session()
    #     g = s.query(TrGroup).get(data['result'])
    #     self.assertEquals(g.title, u'group')
    #     self.assertEquals(g.desc, u'desc')
    #     s.close()

    # def test_add_group_no_desc(self):

    #     self.session.add(self.u1)
    #
    #     data = server.addGroup(self.u1.id, "group", "desc", true, false, false)
    #
    #     self.assertJsonRpc(data)
    #     self.assertIs(type(data['result'], True)


    # @unittest.skip("Add new group.")
    # def test_relations(self):
    #
    #     # TODO: Add some code
    #
    #     data = server.getDevices(self.u1.id)
    #
    #     self.assertIn(u'result', data)
    #     self.assertEquals(len(data['result']), 1)
    #     self.assertEquals(data['result'][0]['sn'], 'EW-14100001-UT')


class GroupDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)  # one own group
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)  # two own groups
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)  # in one group
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)  # in two groups
        cls.u5 = TrUser(login="55555", type="phone", auth_code="5555", authenticated=True)  # no any groups
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4, cls.u5]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.refresh(cls.u5)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2")
        cls.g3 = TrGroup(user_id=cls.u2.id, title="g3")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g1.users.append(cls.u3)
        cls.g1.users.append(cls.u4)
        cls.g2.users.append(cls.u4)
        session.add_all([cls.g1, cls.g2])
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


    def test_delete_one_own_group(self):

        self.session.add(self.u1)
        self.session.add(self.g1)

        data = server.delGroup(self.u1.id, self.g1.id)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)

        """ Separate session, cause cross-session's transaction collision """
        s = Session()
        g = s.query(TrGroup).get(self.g1.id)
        self.assertIsNone(g)
        s.close()

    def test_delete_not_own_group(self):

        self.session.add(self.u3)
        self.session.add(self.g1)

        data = server.delGroup(self.u3.id, self.g1.id)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Group doesn't exist.")

    def test_delete_incorrect_group(self):

        self.session.add(self.u1)
        self.session.add(self.g1)

        data = server.delGroup(self.u1.id, self.g1.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Group doesn't exist.")


class GroupGetGroupMembersTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)  # one own group, not member
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)  # two own groups, not member
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)  # no own groups, member in one group
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)  # no own groups, member in two groups
        cls.u5 = TrUser(login="55555", type="phone", auth_code="5555", authenticated=True)  # one own group, member in one group
        cls.u6 = TrUser(login="66666", type="phone", auth_code="6666", authenticated=True)  # two own groups, member in two groups
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4, cls.u5, cls.u6]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.refresh(cls.u5)
        session.refresh(cls.u6)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2.1")
        cls.g3 = TrGroup(user_id=cls.u2.id, title="g2.2")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g2.users.append(cls.u1)
        session.add_all([cls.g2])
        session.commit()

        session.close()
        
        # TODO: Add tests for group members

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


class CommentAddTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)  # one own group, not member
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)  # two own groups, not member
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)  # no own groups, member in one group
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)  # no own groups, member in two groups
        cls.u5 = TrUser(login="55555", type="phone", auth_code="5555", authenticated=True)  # one own group, member in one group
        cls.u6 = TrUser(login="66666", type="phone", auth_code="6666", authenticated=True)  # two own groups, member in two groups
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4, cls.u5, cls.u6]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.refresh(cls.u5)
        session.refresh(cls.u6)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2.1")
        cls.g3 = TrGroup(user_id=cls.u2.id, title="g2.2")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g2.users.append(cls.u1)
        session.add_all([cls.g2])
        session.commit()

        session.close()
        
        # TODO: Add tests for comments

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


class CommentDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)  # one own group, not member
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)  # two own groups, not member
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)  # no own groups, member in one group
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)  # no own groups, member in two groups
        cls.u5 = TrUser(login="55555", type="phone", auth_code="5555", authenticated=True)  # one own group, member in one group
        cls.u6 = TrUser(login="66666", type="phone", auth_code="6666", authenticated=True)  # two own groups, member in two groups
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4, cls.u5, cls.u6]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.refresh(cls.u5)
        session.refresh(cls.u6)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2.1")
        cls.g3 = TrGroup(user_id=cls.u2.id, title="g2.2")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g2.users.append(cls.u1)
        session.add_all([cls.g2])
        session.commit()

        session.close()
        
        # TODO: Add tests for comments

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


class GroupMeetingsGetTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        """
        u1 - g1 - m1
        u2 - g2 - m2,m3
        u3 - g3 - x
        u4 -> g1, g2, g3
        """
        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2")
        cls.g3 = TrGroup(user_id=cls.u3.id, title="g3")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g1.users.append(cls.u4)
        cls.g2.users.append(cls.u4)
        cls.g3.users.append(cls.u4)
        session.add_all([cls.g1, cls.g2, cls.g3])
        session.commit()

        # Add meetings to groups
        cls.m1 = TrGroupMeeting(group_id=cls.g1.id, title="m1", time="2010-12-12 12:12:12")
        cls.m2 = TrGroupMeeting(group_id=cls.g2.id, title="m2", time="2011-12-12 12:12:12")
        cls.m3 = TrGroupMeeting(group_id=cls.g2.id, title="m3", time="2012-12-12 12:12:12")
        session.add_all([cls.m1, cls.m2, cls.m3])
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


    def test_get_u1_g1_m1(self):

        self.session.add(self.u1)

        data = server.getGroups(self.u1.id)

        self.assertJsonRpc(data)
        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], "g1")
        self.assertEquals(data['result'][0]['admin'], True)
        self.assertEquals(len(data['result'][0]['meetings']), 1)
        self.assertEquals(data['result'][0]['meetings'][0]['title'], u'm1')

    def test_get_u2_g2_m23(self):

        self.session.add(self.u2)

        data = server.getGroups(self.u2.id)

        self.assertJsonRpc(data)
        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 1)
        self.assertEquals(data['result'][0]['title'], "g2")
        self.assertEquals(data['result'][0]['admin'], True)
        self.assertEquals(len(data['result'][0]['meetings']), 2)
        self.assertEquals(data['result'][0]['meetings'][0]['title'], u'm2')
        self.assertEquals(data['result'][0]['meetings'][1]['title'], u'm3')

    def test_get_u4_g123_mX(self):

        self.session.add(self.u4)

        data = server.getGroups(self.u4.id)

        self.assertJsonRpc(data)
        self.assertIn(u'result', data)
        self.assertEquals(len(data['result']), 3)
        self.assertEquals(data['result'][0]['title'], "g1")
        self.assertEquals(data['result'][1]['title'], "g2")
        self.assertEquals(data['result'][2]['title'], "g3")
        self.assertEquals(data['result'][0]['admin'], False)
        self.assertEquals(data['result'][1]['admin'], False)
        self.assertEquals(data['result'][2]['admin'], False)
        self.assertEquals(len(data['result'][0]['meetings']), 1)
        self.assertEquals(len(data['result'][1]['meetings']), 2)
        self.assertIsNone(data['result'][2]['meetings'])
        self.assertEquals(data['result'][0]['meetings'][0]['title'], u'm1')
        self.assertEquals(data['result'][1]['meetings'][0]['title'], u'm2')
        self.assertEquals(data['result'][1]['meetings'][1]['title'], u'm3')


class GroupMeetingAddTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        """
        u1 - g1 - m1
        u2 - g2 - m2,m3
        u3 - g3 - x
        u4 -> g1, g2, g3
        """
        session = Session()

        cls.u1 = TrUser(login="11111", type="phone", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", type="phone", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", type="phone", auth_code="3333", authenticated=True)
        cls.u4 = TrUser(login="44444", type="phone", auth_code="4444", authenticated=True)
        u_list = [cls.u1, cls.u2, cls.u3, cls.u4]
        cls.user_count = len(u_list)
        session.add_all(u_list)
        session.flush()
        session.refresh(cls.u1)
        session.refresh(cls.u2)
        session.refresh(cls.u3)
        session.refresh(cls.u4)
        session.commit()

        cls.g1 = TrGroup(user_id=cls.u1.id, title="g1")
        cls.g2 = TrGroup(user_id=cls.u2.id, title="g2")
        cls.g3 = TrGroup(user_id=cls.u3.id, title="g3")
        g_list = [cls.g1, cls.g2, cls.g3]
        cls.group_count = len(g_list)
        session.add_all(g_list)
        session.commit()

        # Add users to groups
        cls.g1.users.append(cls.u4)
        cls.g2.users.append(cls.u4)
        cls.g3.users.append(cls.u4)
        session.add_all([cls.g1, cls.g2, cls.g3])
        session.commit()

        session.close()

    @classmethod
    def tearDownClass(cls):

        session = Session()

        users = session.query(TrUser).all()
        map(session.delete, users)

        groups = session.query(TrGroup).all()
        map(session.delete, groups)

        session.commit()

        session.close()


    def test_add_notmal_meeting(self):

        self.session.add(self.u1)
        self.session.add(self.g1)

        data = server.addGroupMeeting(self.u1.id, self.g1.id, "t1", "54.123,35.333", 123456789)

        self.assertJsonRpc(data)
        self.assertIn(u'result', data)
        self.assertIs(type(data['result']), int)

        s = Session()
        g = s.query(TrGroup).get(self.g1.id)
        self.assertEquals(len(g.meetings), 1)
        self.assertEquals(g.meetings[0].id, data['result'])
        self.assertEquals(g.meetings[0].title, u't1')
        s.close()


def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(GroupBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupDeleteTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupGetGroupMembersTestCase))
    suite.addTests(loader.loadTestsFromTestCase(CommentAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(CommentDeleteTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupMeetingsGetTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
