# -*- coding: utf-8 -*-

__author__ = 'Anton Glukhov'
__copyright__ = "Copyright 2014, Easywhere"
__email__ = "ag@easywhere.ru"

import unittest
from base import BaseTestCase
from sqlautocode_gen.model import *
from sqlautocode_gen.group_model import TrGroup
from tests.run import Session, server


def setUpModule():
    pass


def tearModuleDown():
    pass


class GroupBaseTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)
        cls.u4 = TrUser(login="44444", auth_code="4444", authenticated=True)
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

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)  # one own group
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)  # two own groups
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)  # in one group
        cls.u4 = TrUser(login="44444", auth_code="4444", authenticated=True)  # in two groups
        cls.u5 = TrUser(login="55555", auth_code="5555", authenticated=True)  # no any groups
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

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)
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

    def test_add_group(self):
    
        self.session.add(self.u1)

        data = server.addGroup(self.u1.id, "group", "desc", true, false, false)

        self.assertJsonRpc(data)
        self.assertIs(data['result'], True)
        

    def test_add_group_no_desc(self):

        self.session.add(self.u1)
        
        data = server.addGroup(self.u1.id, "group", None, true, false, false)
        
        self.assertJsonRpc(data)
        self.assertIs(type(data['result'], True)



class GroupDeleteTestCase(BaseTestCase):

    @classmethod
    def setUpClass(cls):

        session = Session()

        cls.u1 = TrUser(login="11111", auth_code="1111", authenticated=True)  # one own group
        cls.u2 = TrUser(login="22222", auth_code="2222", authenticated=True)  # two own groups
        cls.u3 = TrUser(login="33333", auth_code="3333", authenticated=True)  # in one group
        cls.u4 = TrUser(login="44444", auth_code="4444", authenticated=True)  # in two groups
        cls.u5 = TrUser(login="55555", auth_code="5555", authenticated=True)  # no any groups
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

    def test_delete_incorrect_group(self):

        self.session.add(self.u1)
        self.session.add(self.g1)

        data = server.delGroup(self.u1.id, self.g1.id + 1000)

        self.assertJsonRpcErr(data)
        self.assertEquals(data['error'][u'message'], "ServerError: Group doesn't exist.")


class GroupMessageAddTestCase(BaseTestCase):
    #TODO: source here
    
class GroupMessageDeleteCase(BaseTestCase):
    #TODO: source here
    

def suite():

    loader = unittest.TestLoader()
    suite = unittest.TestSuite()

    suite.addTests(loader.loadTestsFromTestCase(GroupBaseTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupGetTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupAddTestCase))
    suite.addTests(loader.loadTestsFromTestCase(GroupDeleteTestCase))

    return suite


if __name__ == '__main__':
    unittest.main(defaultTest='suite')
